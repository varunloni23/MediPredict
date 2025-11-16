import pandas as pd
import numpy as np
from app.ml.model import DeviceHealthPredictor

def create_training_data():
    """
    Create sample training data with labels
    """
    # Generate sample data
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'usage_hours': np.random.uniform(0, 1000, n_samples),
        'temperature': np.random.uniform(20, 60, n_samples),
        'pressure': np.random.uniform(50, 200, n_samples),
        'vibration': np.random.uniform(0, 2, n_samples),
        'error_count': np.random.poisson(2, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create labels based on realistic rules
    # Healthy devices: low error count, normal temperature, low vibration
    # At risk: medium error count, higher temperature or vibration
    # Needs maintenance: high error count, high temperature, high vibration
    
    conditions = [
        (df['error_count'] <= 1) & (df['temperature'] <= 35) & (df['vibration'] <= 0.3),
        (df['error_count'] > 1) & (df['error_count'] <= 5) & ((df['temperature'] > 35) | (df['vibration'] > 0.3)),
        (df['error_count'] > 5) | (df['temperature'] > 45) | (df['vibration'] > 0.8)
    ]
    
    choices = ['healthy', 'at_risk', 'needs_maintenance']
    df['health_status'] = np.select(conditions, choices, default='healthy')
    
    return df

def train_model():
    """
    Train the device health prediction model
    """
    # Create training data
    print("Creating training data...")
    df = create_training_data()
    
    # Initialize predictor
    predictor = DeviceHealthPredictor()
    
    # Train the model
    print("Training model...")
    model = predictor.train(df, target_column='health_status')
    
    # Test the model
    print("Testing model with sample data...")
    test_data = pd.DataFrame({
        'usage_hours': [100, 500, 800],
        'temperature': [30, 45, 55],
        'pressure': [100, 150, 180],
        'vibration': [0.1, 0.5, 1.2],
        'error_count': [0, 3, 8]
    })
    
    predictions = predictor.predict(test_data)
    
    print("\nSample Predictions:")
    for i, (status, confidence, recommendation) in enumerate(predictions):
        print(f"Device {i+1}: {status} (confidence: {confidence:.2f})")
        print(f"  Recommendation: {recommendation}")
    
    print("\nModel training completed and saved!")

if __name__ == "__main__":
    train_model()