from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from app.database import get_db
from app.ml.model import predictor
from app.crud import device_data as crud_device_data

router = APIRouter()

class PredictionRequest(BaseModel):
    device_id: str
    usage_hours: Optional[float] = 0
    temperature: Optional[float] = 0
    pressure: Optional[float] = 0
    vibration: Optional[float] = 0
    error_count: Optional[int] = 0

class ExplainablePredictionRequest(BaseModel):
    data: List[PredictionRequest]

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

@router.post("/predict-explainable")
def predict_with_explanation(request: ExplainablePredictionRequest, db: Session = Depends(get_db)):
    """
    Make predictions with detailed explanations including feature importance
    """
    try:
        # Convert request data to DataFrame
        data_dicts = []
        for item in request.data:
            data_dicts.append({
                'usage_hours': item.usage_hours or 0,
                'temperature': item.temperature or 0,
                'pressure': item.pressure or 0,
                'vibration': item.vibration or 0,
                'error_count': item.error_count or 0
            })
        
        df = pd.DataFrame(data_dicts)
        
        # Get predictions with explanations
        predictions = predictor.predict_with_explanation(df)
        
        # Add device IDs to results
        for idx, pred in enumerate(predictions):
            pred['device_id'] = request.data[idx].device_id
        
        return {
            "predictions": predictions,
            "count": len(predictions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/explain/{device_id}")
def explain_device_prediction(device_id: str, db: Session = Depends(get_db)):
    """
    Get explainable prediction for a specific device using its latest data
    """
    try:
        # Get the latest device data
        latest_data = crud_device_data.get_device_data_by_device_id(db, device_id=device_id, limit=1)
        
        if not latest_data:
            raise HTTPException(status_code=404, detail="No data found for this device")
        
        # Convert to DataFrame
        data = latest_data[0]
        df = pd.DataFrame([{
            'usage_hours': data.usage_hours or 0,
            'temperature': data.temperature or 0,
            'pressure': data.pressure or 0,
            'vibration': data.vibration or 0,
            'error_count': data.error_count or 0
        }])
        
        # Get prediction with explanation
        predictions = predictor.predict_with_explanation(df)
        
        result = predictions[0]
        result['device_id'] = device_id
        result['timestamp'] = data.timestamp.isoformat()
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation generation failed: {str(e)}")

@router.get("/feature-importance")
def get_global_feature_importance():
    """
    Get global feature importance from the trained model
    """
    try:
        if not predictor.is_trained or predictor.model is None:
            if not predictor.load_model():
                raise HTTPException(status_code=400, detail="No trained model available")
        
        if predictor.model is None:
            raise HTTPException(status_code=400, detail="Model not available")
        
        # Get feature importance
        feature_importance = predictor.model.feature_importances_
        
        # Create feature importance dictionary
        importance_dict = {}
        for feature_name, importance in zip(predictor.feature_names, feature_importance):
            importance_dict[feature_name] = float(importance)
        
        # Sort by importance
        sorted_importance = sorted(
            importance_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "feature_importance": dict(sorted_importance),
            "interpretation": {
                "usage_hours": "Total hours the device has been in operation",
                "temperature": "Operating temperature in degrees Celsius",
                "pressure": "Operating pressure in PSI",
                "vibration": "Vibration frequency in Hz",
                "error_count": "Number of errors recorded"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get feature importance: {str(e)}")