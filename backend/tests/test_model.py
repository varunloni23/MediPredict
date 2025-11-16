import pandas as pd
import numpy as np
from app.ml.model import DeviceHealthPredictor

def test_model():
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'usage_hours': [100, 200, 300, 150, 250],
        'temperature': [30, 35, 40, 32, 38],
        'pressure': [100, 120, 140, 110, 130],
        'vibration': [0.1, 0.2, 0.5, 0.15, 0.4],
        'error_count': [0, 1, 5, 0, 3]
    })
    
    # Initialize predictor
    predictor = DeviceHealthPredictor()
    
    # Test prediction (this will fail since we don't have a trained model)
    try:
        predictions = predictor.predict(sample_data)
        print("Predictions:", predictions)
    except Exception as e:
        print(f"Error during prediction: {e}")
        print("This is expected since we don't have a trained model yet.")

if __name__ == "__main__":
    test_model()