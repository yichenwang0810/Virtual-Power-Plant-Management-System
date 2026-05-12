# backend/optimizer.py
import numpy as np
from scipy.optimize import minimize
import yaml

class VPPScheduler:
    def __init__(self, config_path='config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.bat_cap = self.config['system']['battery']['capacity_kwh']
        self.bat_p_max = self.config['system']['battery']['max_power_kw']
        self.eff = self.config['system']['battery']['efficiency']

    def optimize(self, load_data, pv_data, dr_event=False):
        load = np.array([x['load_kw'] for x in load_data])
        pv = np.array([x['pv_kw'] for x in pv_data])
        prices = self.config['market']

        # Objective Function
        def objective(dispatch):
            total_cost = 0
            for t in range(24):
                p_bat = dispatch[t]
                p_grid = load[t] - pv[t] + p_bat
                
                # --- DEMAND RESPONSE LOGIC ---
                if dr_event:
                    # Penalty for not discharging during DR
                    # We want p_bat to be negative (discharge)
                    penalty = max(0, p_bat) * 1000 
                    total_cost += penalty 
                else:
                    # Normal Economic Dispatch
                    if p_grid > 0: total_cost += p_grid * prices['buy'][t]
                    else: total_cost += p_grid * prices['sell'][t]
            return total_cost

        bnds = [(-self.bat_p_max, self.bat_p_max) for _ in range(24)]
        x0 = np.zeros(24)

        result = minimize(objective, x0, method='SLSQP', bounds=bnds)
        
        # Return simple schedule
        return [{"hour": f"{i:02d}:00", "battery_kw": round(result.x[i], 2)} for i in range(24)]