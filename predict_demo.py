#!/usr/bin/env python3
"""
Example script showing how to use MediPredict for device health predictions
"""

import sys
import os
import pandas as pd

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def create_sample_device_data():
    """Create sample device data for prediction"""
    # Sample data for different devices
    sample_data = pd.DataFrame({
        'device_id': ['DEV-001', 'DEV-002', 'DEV-003', 'DEV-004', 'DEV-005'],
        'usage_hours': [120.5, 450.2, 780.1, 85.3, 320.7],
        'temperature': [32.1, 45.5, 52.3, 29.8, 38.2],
        'pressure': [105.2, 155.7, 178.9, 98.4, 132.6],
        'vibration': [0.15, 0.65, 1.25, 0.08, 0.42],
        'error_count': [0, 3, 7, 0, 2]
    })
    return sample_data

def predict_device_health():
    """Make predictions for sample devices"""
    print("Making predictions for sample devices...")
    
    try:
        from backend.app.ml.model import predictor
        
        # Create sample data
        sample_data = create_sample_device_data()
        
        # For prediction, we only need the feature columns
        feature_data = pd.DataFrame({
            'usage_hours': sample_data['usage_hours'],
            'temperature': sample_data['temperature'],
            'pressure': sample_data['pressure'],
            'vibration': sample_data['vibration'],
            'error_count': sample_data['error_count']
        })
        
        # Make predictions
        predictions = predictor.predict(feature_data)
        
        print("\nDevice Health Predictions:")
        print("-" * 50)
        for i, (status, confidence, recommendation) in enumerate(predictions):
            device_id = sample_data.iloc[i]['device_id']
            usage_hours = sample_data.iloc[i]['usage_hours']
            temp = sample_data.iloc[i]['temperature']
            errors = sample_data.iloc[i]['error_count']
            
            print(f"Device ID: {device_id}")
            print(f"  Usage: {usage_hours} hours | Temp: {temp}°C | Errors: {errors}")
            print(f"  Status: {status.upper()}")
            print(f"  Confidence: {confidence:.2f}")
            print(f"  Recommendation: {recommendation}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def save_sample_data_to_csv():
    """Save sample data to CSV file"""
    sample_data = create_sample_device_data()
    csv_file = "sample_device_data.csv"
    sample_data.to_csv(csv_file, index=False)
    print(f"Sample data saved to {csv_file}")
    return csv_file

def main():
    print("MediPredict Device Health Prediction Demo")
    print("=" * 50)
    
    # Save sample data to CSV
    csv_file = save_sample_data_to_csv()
    print()
    
    # Make predictions
    success = predict_device_health()
    
    if success:
        print("🎉 Device health predictions completed successfully!")
        print(f"\nYou can find the sample data in: {csv_file}")
        print("\nIn a production environment, you would:")
        print("1. Upload CSV files with device data through the web interface")
        print("2. The system would automatically preprocess the data")
        print("3. The ML model would generate health predictions")
        print("4. Results would be displayed in the dashboard")
    else:
        print("❌ Prediction demo failed.")

if __name__ == "__main__":
    main()