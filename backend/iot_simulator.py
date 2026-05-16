# backend/iot_simulator.py
import time
import random
import threading
from backend.database import SessionLocal, BatteryStatus, EnergyLog
from datetime import datetime

def simulate_battery_loop():
    db = SessionLocal()
    current_soc = 50.0 # Start at 50%
    
    print("🔋 IoT Simulator Started...")
    
    while True:
        # 1. Read current schedule (Mocking an API call to main.py)
        # In a real app, you would fetch the schedule for the current hour
        # Here we just simulate random fluctuation around a setpoint
        target_power = random.uniform(-50, 50) 
        
        # 2. Update Physics
        # Simple physics: Power * time = Energy change
        # Assuming 1 sec loop ~ negligible change, so we add noise
        change = (target_power / 1000) * 0.1 # rough approximation
        current_soc += change
        current_soc = max(0, min(100, current_soc)) # Clamp 0-100%

        # 3. Determine Mode
        mode = "IDLE"
        if target_power > 1: mode = "CHARGE"
        elif target_power < -1: mode = "DISCHARGE"

        # 4. Save to DB
        new_reading = BatteryStatus(soc_percent=current_soc, power_kw=target_power, mode=mode)
        db.add(new_reading)
        
        # Mock Energy Log
        log = EnergyLog(pv_generation=random.uniform(0, 10), load_consumption=random.uniform(5, 20), cost=random.uniform(1, 5))
        db.add(log)
        
        db.commit()
        time.sleep(2) # Update every 2 seconds for demo speed

def start_simulator():
    thread = threading.Thread(target=simulate_battery_loop, daemon=True)
    thread.start()