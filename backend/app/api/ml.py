from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.database import get_db
from app.ml.model import predictor
from app.crud import device_data as crud_device_data

router = APIRouter()

@router.post("/train-model")
def train_model(db: Session = Depends(get_db)):
    """
    Train the device health prediction model with existing data
    """
    try:
        # Get all device data from database
        all_device_data = crud_device_data.get_all_device_data(db, limit=10000)
        
        if not all_device_data:
            raise HTTPException(status_code=400, detail="No device data available for training")
        
        # Convert to DataFrame
        data_dicts = []
        for data in all_device_data:
            data_dicts.append({
                'usage_hours': data.usage_hours,
                'temperature': data.temperature,
                'pressure': data.pressure,
                'vibration': data.vibration,
                'error_count': data.error_count,
                'health_status': 'healthy'  # This would need to be determined or provided
            })
        
        df = pd.DataFrame(data_dicts)
        
        # For demonstration, we'll randomly assign health statuses
        # In a real application, these would come from historical maintenance records
        import numpy as np
        conditions = [
            (df['error_count'] <= 1) & (df['temperature'] <= 35) & (df['vibration'] <= 0.3),
            (df['error_count'] > 1) & (df['error_count'] <= 5) & ((df['temperature'] > 35) | (df['vibration'] > 0.3)),
            (df['error_count'] > 5) | (df['temperature'] > 45) | (df['vibration'] > 0.8)
        ]
        
        choices = ['healthy', 'at_risk', 'needs_maintenance']
        df['health_status'] = np.select(conditions, choices, default='healthy')
        
        # Train the model
        model = predictor.train(df, target_column='health_status')
        
        return {
            "message": "Model trained successfully",
            "records_used": len(df),
            "model_saved": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")