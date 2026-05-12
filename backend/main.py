# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db, BatteryStatus, EnergyLog
from optimizer import VPPScheduler
from data_loader import get_daily_profiles
from iot_simulator import start_simulator
from finance import FinanceManager
from alerts import alert_system
from forecaster import LoadForecaster

app = FastAPI(title="VPP Enterprise System")

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Initialize Components
start_simulator()
scheduler = VPPScheduler()
finance = FinanceManager()
forecaster = LoadForecaster()

# --- Endpoints ---

@app.get("/telemetry")
def get_live_telemetry(db: Session = Depends(get_db)):
    latest = db.query(BatteryStatus).order_by(BatteryStatus.id.desc()).first()
    if not latest: return {"soc": 0, "power": 0, "mode": "OFFLINE"}
    
    # Check for critical alerts automatically
    if latest.soc_percent < 10:
        alert_system.trigger_alert("Battery Critical Low (<10%)", "CRITICAL")
    elif latest.soc_percent > 95:
        alert_system.trigger_alert("Battery Full, stopping charge", "WARNING")
        
    return {"soc": round(latest.soc_percent, 2), "power": round(latest.power_kw, 2), "mode": latest.mode}

@app.get("/dispatch")
def get_dispatch_plan(dr_active: bool = False):
    data = get_daily_profiles()
    schedule = scheduler.optimize(data, data, dr_event=dr_active)
    
    if dr_active:
        alert_system.trigger_alert("⚠️ DEMAND RESPONSE EVENT ACTIVE", "CRITICAL")
    else:
        alert_system.trigger_alert("Optimization Run Complete", "INFO")
        
    return {"status": "success", "dr_active": dr_active, "data": schedule}

@app.get("/finance")
def get_financials(db: Session = Depends(get_db)):
    return finance.calculate_session_pnl(db)

@app.get("/alerts")
def get_alerts():
    return alert_system.get_alerts()

@app.get("/forecast")
def get_forecast():
    # Mock historical data input
    history = [] 
    return forecaster.predict_tomorrow(history)