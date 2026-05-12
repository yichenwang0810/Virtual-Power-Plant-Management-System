# backend/alerts.py
import time
from threading import Thread

class AlertManager:
    def __init__(self):
        self.active_alerts = []

    def trigger_alert(self, message, severity="INFO"):
        alert = {
            "id": int(time.time()),
            "message": message,
            "severity": severity, # INFO, WARNING, CRITICAL
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.active_alerts.insert(0, alert) # Add to top
        # Keep only last 5 alerts
        self.active_alerts = self.active_alerts[:5]
        print(f"🚨 ALERT [{severity}]: {message}")

    def get_alerts(self):
        return self.active_alerts

    def clear_alerts(self):
        self.active_alerts = []

# Global instance
alert_system = AlertManager()