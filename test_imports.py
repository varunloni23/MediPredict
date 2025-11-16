import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    # Test importing the main modules
    from backend.app.main import app
    print("✅ FastAPI app imported successfully")
    
    # Test database connection
    from backend.app.database import engine
    print("✅ Database module imported successfully")
    
    # Test ML model
    from backend.app.ml.model import predictor
    print("✅ ML model imported successfully")
    
    print("\n🎉 All core components imported successfully!")
    print("\nTo run the full application, try:")
    print("  cd backend && python3 run.py")
    
except Exception as e:
    print(f"❌ Error importing components: {e}")
    import traceback
    traceback.print_exc()