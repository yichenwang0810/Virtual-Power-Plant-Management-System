# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from optimizer import VPPScheduler
from data_loader import get_daily_profiles

app = FastAPI(title="VPP Management System")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Scheduler
scheduler = VPPScheduler()

@app.get("/")
def read_root():
    return {"message": "VPP System Running. Go to /dispatch for schedule."}

@app.get("/dispatch")
def get_dispatch_plan():
    # 1. Get Load/PV Data
    data = get_daily_profiles()
    
    # 2. Run Optimization
    schedule = scheduler.optimize(data, data) # Using same data for simplicity
    
    # 3. Return JSON
    return {
        "status": "success",
        "data": schedule
    }