# backend/forecaster.py
import numpy as np

class LoadForecaster:
    def predict_tomorrow(self, historical_data):
        """
        In a real app, this would use LSTM or Prophet.
        Here we simulate a prediction with some noise.
        """
        # Mock prediction: Similar to historical average but shifted
        base_load = [40, 30, 20, 20, 30, 50, 90, 140, 190, 210, 200, 190,
                     170, 180, 190, 200, 220, 240, 210, 170, 140, 110, 70, 50]
        
        # Add random noise to simulate uncertainty
        noise = np.random.normal(0, 5, 24)
        prediction = np.array(base_load) + noise
        
        return [{"hour": f"{i:02d}:00", "predicted_load_kw": round(prediction[i], 2)} for i in range(24)]