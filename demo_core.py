#!/usr/bin/env python3
"""
Demo script to show MediPredict core functionality
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def init_database():
    """Initialize the database tables"""
    print("Initializing database...")
    try:
        from backend.app.database import Base, engine
        from backend.app.models import user, device, device_data, prediction
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_ml_training():
    """Test ML model training with sample data"""
    print("Testing ML model training...")
    try:
        import pandas as pd
        import numpy as np
        from backend.app.ml.model import predictor
        
        # Create sample training data
        np.random.seed(42)
        n_samples = 100
        
        data = {
            'usage_hours': np.random.uniform(0, 1000, n_samples),
            'temperature': np.random.uniform(20, 60, n_samples),
            'pressure': np.random.uniform(50, 200, n_samples),
            'vibration': np.random.uniform(0, 2, n_samples),
            'error_count': np.random.poisson(2, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create labels based on realistic rules
        conditions = [
            (df['error_count'] <= 1) & (df['temperature'] <= 35) & (df['vibration'] <= 0.3),
            (df['error_count'] > 1) & (df['error_count'] <= 5) & ((df['temperature'] > 35) | (df['vibration'] > 0.3)),
            (df['error_count'] > 5) | (df['temperature'] > 45) | (df['vibration'] > 0.8)
        ]
        
        choices = ['healthy', 'at_risk', 'needs_maintenance']
        df['health_status'] = np.select(conditions, choices, default='healthy')
        
        # Train the model
        model = predictor.train(df, target_column='health_status')
        print("✅ ML model trained successfully!")
        
        # Test predictions
        test_data = pd.DataFrame({
            'usage_hours': [100, 500, 800],
            'temperature': [30, 45, 55],
            'pressure': [100, 150, 180],
            'vibration': [0.1, 0.5, 1.2],
            'error_count': [0, 3, 8]
        })
        
        predictions = predictor.predict(test_data)
        print("Sample predictions:")
        for i, (status, confidence, recommendation) in enumerate(predictions):
            print(f"  Device {i+1}: {status} (confidence: {confidence:.2f})")
        
        return True
    except Exception as e:
        print(f"❌ ML training failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("MediPredict Core Functionality Demo")
    print("=" * 40)
    
    # Test database initialization
    db_success = init_database()
    print()
    
    # Test ML training
    ml_success = test_ml_training()
    print()
    
    if db_success and ml_success:
        print("🎉 All core functionality is working!")
        print("\nYou can now:")
        print("1. Use the database with your Supabase connection")
        print("2. Make predictions with the trained ML model")
        print("\nTo run the full web application, you may need to resolve")
        print("the FastAPI version compatibility issues.")
    else:
        print("❌ Some core functionality failed.")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()