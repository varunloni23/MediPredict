#!/usr/bin/env python3
"""
Demo script to show the complete MediPredict workflow
"""

import os
import sys
import time
import pandas as pd
from backend.app.ml.model import DeviceHealthPredictor
from backend.generate_sample_data import generate_sample_data

def demo_workflow():
    print("=== MediPredict Demo Workflow ===\n")
    
    # Step 1: Generate sample data
    print("1. Generating sample device data...")
    sample_data = generate_sample_data(num_devices=3, records_per_device=50)
    print(f"   Generated {len(sample_data)} records for {sample_data['device_id'].nunique()} devices\n")
    
    # Step 2: Save data to CSV
    print("2. Saving data to CSV file...")
    sample_data.to_csv("sample_data.csv", index=False)
    print("   Data saved to sample_data.csv\n")
    
    # Step 3: Train model
    print("3. Training predictive model...")
    predictor = DeviceHealthPredictor()
    
    # Add health status labels for training
    import numpy as np
    conditions = [
        (sample_data['error_count'] <= 1) & (sample_data['temperature'] <= 35) & (sample_data['vibration'] <= 0.3),
        (sample_data['error_count'] > 1) & (sample_data['error_count'] <= 5) & ((sample_data['temperature'] > 35) | (sample_data['vibration'] > 0.3)),
        (sample_data['error_count'] > 5) | (sample_data['temperature'] > 45) | (sample_data['vibration'] > 0.8)
    ]
    
    choices = ['healthy', 'at_risk', 'needs_maintenance']
    sample_data['health_status'] = np.select(conditions, choices, default='healthy')
    
    # Train the model
    model = predictor.train(sample_data, target_column='health_status')
    print("   Model trained successfully!\n")
    
    # Step 4: Make predictions
    print("4. Making predictions on new data...")
    # Create some new test data
    test_data = pd.DataFrame({
        'usage_hours': [120, 450, 780],
        'temperature': [32, 48, 52],
        'pressure': [110, 165, 185],
        'vibration': [0.2, 0.7, 1.3],
        'error_count': [1, 4, 9]
    })
    
    predictions = predictor.predict(test_data)
    
    print("   Predictions:")
    for i, (status, confidence, recommendation) in enumerate(predictions):
        print(f"   Device {i+1}: {status.upper()} (confidence: {confidence:.2f})")
        print(f"     Recommendation: {recommendation}")
    print()
    
    # Step 5: Summary
    print("5. Demo completed successfully!")
    print("   - Sample data generated and saved")
    print("   - Model trained on sample data")
    print("   - Predictions made on new data")
    print("\nTo run the full web application:")
    print("   1. Start the backend: cd backend && python run.py")
    print("   2. Start the frontend: cd frontend && npm run dev")
    print("   3. Visit http://localhost:3000 in your browser")

if __name__ == "__main__":
    demo_workflow()