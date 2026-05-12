# backend/data_loader.py
import numpy as np
import pandas as pd

def get_daily_profiles():
    """
    Generates mock data for Load (kW) and PV (kW) for 24 hours.
    """
    hours = 24
    time_range = pd.date_range(start='00:00', periods=hours, freq='H')
    
    # Simulate Load: Higher during day, lower at night
    load_profile = [50, 40, 30, 30, 40, 60, 100, 150, 200, 220, 210, 200, 
                    180, 190, 200, 210, 230, 250, 220, 180, 150, 120, 80, 60]
    
    # Simulate PV: Bell curve around noon
    pv_profile = [0, 0, 0, 0, 0, 0, 10, 50, 100, 150, 180, 190, 
                  180, 150, 100, 50, 20, 0, 0, 0, 0, 0, 0, 0]

    df = pd.DataFrame({
        "time": time_range,
        "load_kw": load_profile,
        "pv_kw": pv_profile
    })
    return df.to_dict('records')