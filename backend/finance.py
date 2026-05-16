# backend/finance.py
from datetime import datetime
from backend.database import SessionLocal, EnergyLog, BatteryStatus

class FinanceManager:
    def __init__(self):
        self.revenue_log = []

    def calculate_session_pnl(self, db: SessionLocal):
        # Fetch last 10 energy logs
        logs = db.query(EnergyLog).order_by(EnergyLog.id.desc()).limit(10).all()
        
        total_cost = 0
        total_revenue = 0
        
        for log in logs:
            # Simple logic: Negative cost is revenue
            if log.cost < 0:
                total_revenue += abs(log.cost)
            else:
                total_cost += log.cost
                
        net_profit = total_revenue - total_cost
        return {
            "gross_cost": round(total_cost, 2),
            "gross_revenue": round(total_revenue, 2),
            "net_profit": round(net_profit, 2)
        }

    def estimate_future_savings(self, forecast_accuracy):
        # Mock logic: Better forecast = higher savings
        base_savings = 50.0
        return base_savings * (1 + (forecast_accuracy / 100))