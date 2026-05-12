# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db, BatteryStatus, EnergyLog
from optimizer import VPPScheduler
from data_loader import get_daily_profiles
from iot_simulator import start_simulator # Import simulator

app = FastAPI(title="VPP Pro System")

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Start the IoT Simulator in the background
start_simulator()

scheduler = VPPScheduler()

@app.get("/telemetry")
def get_live_telemetry(db: Session = Depends(get_db)):
    # Get the latest battery reading
    latest = db.query(BatteryStatus).order_by(BatteryStatus.id.desc()).first()
    if not latest: return {"soc": 0, "power": 0, "mode": "OFFLINE"}
    return {
        "soc": round(latest.soc_percent, 2),
        "power": round(latest.power_kw, 2),
        "mode": latest.mode,
        "timestamp": latest.timestamp
    }

@app.get("/dispatch")
def get_dispatch_plan(dr_active: bool = False):
    data = get_daily_profiles()
    # Pass dr_active flag to optimizer
    schedule = scheduler.optimize(data, data, dr_event=dr_active)
    return {"status": "success", "dr_active": dr_active, "data": schedule}

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    # Get last 10 logs
    logs = db.query(EnergyLog).order_by(EnergyLog.id.desc()).limit(10).all()
    return logs