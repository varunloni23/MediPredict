from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from app.crud import prediction as crud_prediction, device_data as crud_device_data
from app.schemas.prediction import Prediction, PredictionCreate, PredictionUpdate, PredictionResult, BulkPredictionRequest
from app.schemas.device_data import DeviceData
from app.database import get_db
from app.ml.model import predictor
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Prediction)
def create_prediction(prediction: PredictionCreate, db: Session = Depends(get_db)):
    return crud_prediction.create_prediction(db=db, prediction=prediction)

@router.get("/{prediction_id}", response_model=Prediction)
def read_prediction(prediction_id: int, db: Session = Depends(get_db)):
    db_prediction = crud_prediction.get_prediction(db, prediction_id=prediction_id)
    if db_prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return db_prediction

@router.get("/device/{device_id}", response_model=List[Prediction])
def read_predictions_by_device(device_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    predictions = crud_prediction.get_predictions_by_device_id(db, device_id=device_id, skip=skip, limit=limit)
    return predictions

@router.get("/", response_model=List[PredictionResult])
def read_predictions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Get recent predictions (default implementation returns all)
    predictions = crud_prediction.get_recent_predictions(db)
    # Apply pagination manually if needed
    return predictions[skip:skip+limit] if predictions else []

@router.put("/{prediction_id}", response_model=Prediction)
def update_prediction(prediction_id: int, prediction: PredictionUpdate, db: Session = Depends(get_db)):
    db_prediction = crud_prediction.update_prediction(db, prediction_id=prediction_id, prediction_update=prediction)
    if db_prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return db_prediction

@router.delete("/{prediction_id}", response_model=Prediction)
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    db_prediction = crud_prediction.delete_prediction(db, prediction_id=prediction_id)
    if db_prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return db_prediction

@router.post("/predict-for-device/{device_id}", response_model=Prediction)
def predict_for_device(device_id: str, db: Session = Depends(get_db)):
    """
    Generate a prediction for a specific device using its latest data
    """
    # Get the latest device data
    device_data_list = crud_device_data.get_device_data_by_device_id(db, device_id=device_id, limit=10)
    
    if not device_data_list:
        raise HTTPException(status_code=404, detail="No data found for this device")
    
    # Convert to DataFrame for ML model
    data_dicts = []
    for data in device_data_list:
        data_dicts.append({
            'usage_hours': data.usage_hours,
            'temperature': data.temperature,
            'pressure': data.pressure,
            'vibration': data.vibration,
            'error_count': data.error_count
        })
    
    df = pd.DataFrame(data_dicts)
    
    # Make prediction
    try:
        predictions = predictor.predict(df)
        # Use the first prediction (most recent data)
        predicted_status, confidence_score, recommendation = predictions[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # Save prediction to database
    prediction_create = PredictionCreate(
        device_id=device_id,
        predicted_status=predicted_status,
        confidence_score=float(confidence_score),
        features_used=str(df.columns.tolist()),
        recommendation=recommendation
    )
    
    return crud_prediction.create_prediction(db=db, prediction=prediction_create)

@router.post("/bulk-predict", response_model=List[Prediction])
def bulk_predict(request: BulkPredictionRequest, db: Session = Depends(get_db)):
    """
    Generate predictions for multiple devices
    """
    predictions = []
    
    for device_id in request.device_ids:
        try:
            # Get the latest device data
            device_data_list = crud_device_data.get_device_data_by_device_id(db, device_id=device_id, limit=10)
            
            if not device_data_list:
                continue  # Skip devices with no data
            
            # Convert to DataFrame for ML model
            data_dicts = []
            for data in device_data_list:
                data_dicts.append({
                    'usage_hours': data.usage_hours,
                    'temperature': data.temperature,
                    'pressure': data.pressure,
                    'vibration': data.vibration,
                    'error_count': data.error_count
                })
            
            df = pd.DataFrame(data_dicts)
            
            # Make prediction
            pred_results = predictor.predict(df)
            # Use the first prediction (most recent data)
            predicted_status, confidence_score, recommendation = pred_results[0]
            
            # Save prediction to database
            prediction_create = PredictionCreate(
                device_id=device_id,
                predicted_status=predicted_status,
                confidence_score=float(confidence_score),
                features_used=str(df.columns.tolist()),
                recommendation=recommendation
            )
            
            db_prediction = crud_prediction.create_prediction(db=db, prediction=prediction_create)
            predictions.append(db_prediction)
            
        except Exception as e:
            # Log error but continue with other devices
            print(f"Error predicting for device {device_id}: {str(e)}")
            continue
    
    return predictions