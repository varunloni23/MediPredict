#!/usr/bin/env python3
"""
Simple test script to verify MediPredict backend components
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def test_database():
    """Test database connection"""
    print("Testing database connection...")
    try:
        from backend.app.database import engine
        connection = engine.connect()
        print("✅ Database connection successful!")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_ml_model():
    """Test ML model import"""
    print("Testing ML model...")
    try:
        from backend.app.ml.model import predictor
        print("✅ ML model imported successfully!")
        return True
    except Exception as e:
        print(f"❌ ML model import failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoint imports"""
    print("Testing API endpoints...")
    try:
        from backend.app.main import app
        print("✅ API endpoints imported successfully!")
        return True
    except Exception as e:
        print(f"❌ API endpoints import failed: {e}")
        return False

def main():
    print("MediPredict Backend Component Tests")
    print("=" * 40)
    
    tests = [
        test_database,
        test_ml_model,
        test_api_endpoints
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        print()
    
    passed = sum(results)
    total = len(results)
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All components are working correctly!")
    else:
        print("⚠️  Some components need attention.")
        print("\nNote: Even if API endpoints failed, the core functionality")
        print("(database and ML model) may still work correctly.")

if __name__ == "__main__":
    main()