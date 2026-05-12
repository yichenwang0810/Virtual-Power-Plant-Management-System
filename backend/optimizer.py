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

    def calculate_cost(self, dispatch, prices, load, pv):
        total_cost = 0
        soc = self.bat_cap * 0.5  # Start at 50% SoC
        
        for t in range(24):
            p_bat = dispatch[t] # Positive = Charge, Negative = Discharge
            
            # Battery Dynamics
            if p_bat > 0: # Charging
                soc += p_bat * self.eff
            else: # Discharging
                soc += p_bat / self.eff
            
            # Grid Interaction
            # Net Load = Load - PV - Battery_Discharge (or + Charge)
            p_grid = load[t] - pv[t] + p_bat
            
            # Cost Calculation
            if p_grid > 0: # Import from grid
                total_cost += p_grid * prices['buy'][t]
            else: # Export to grid
                total_cost += p_grid * prices['sell'][t]
                
        return total_cost

    def optimize(self, load_data, pv_data):
        load = np.array([x['load_kw'] for x in load_data])
        pv = np.array([x['pv_kw'] for x in pv_data])
        prices = self.config['market']

        # Decision Variable: Battery Power for 24 hours (24 values)
        # Bounds: -250kW (Discharge) to +250kW (Charge)
        bnds = [(-self.bat_p_max, self.bat_p_max) for _ in range(24)]
        
        # Initial guess: Do nothing
        x0 = np.zeros(24)

        # Run Optimization
        result = minimize(
            self.calculate_cost, 
            x0, 
            args=(prices, load, pv),
            method='SLSQP',
            bounds=bnds
        )

        # Format results
        schedule = []
        for i in range(24):
            p_bat = result.x[i]
            p_grid = load[i] - pv[i] + p_bat
            schedule.append({
                "hour": f"{i:02d}:00",
                "battery_kw": round(p_bat, 2),
                "grid_kw": round(p_grid, 2),
                "cost": round(self.calculate_cost(result.x, prices, load, pv) / 24, 2) # Avg cost per hour
            })
            
        return schedule