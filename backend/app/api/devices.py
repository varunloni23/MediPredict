from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from datetime import datetime
from app.crud import device as crud_device, device_data as crud_device_data, prediction as crud_prediction
from app.schemas.device import Device, DeviceCreate, DeviceUpdate
from app.schemas.device_data import DeviceData, DeviceDataCreate, DeviceDataUpload
from app.schemas.prediction import PredictionCreate
from app.database import get_db
from app.ml.model import predictor

router = APIRouter()

@router.post("/", response_model=Device)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = crud_device.get_device_by_device_id(db, device_id=device.device_id)
    if db_device:
        raise HTTPException(status_code=400, detail="Device ID already registered")
    return crud_device.create_device(db=db, device=device)

@router.get("/{device_id}", response_model=Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud_device.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.get("/", response_model=List[Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud_device.get_devices(db, skip=skip, limit=limit)
    return devices

@router.put("/{device_id}", response_model=Device)
def update_device(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db)):
    db_device = crud_device.update_device(db, device_id=device_id, device_update=device)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.delete("/{device_id}", response_model=Device)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud_device.delete_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.post("/{device_id}/upload-data")
async def upload_device_data(device_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Check if device exists, if not create a minimal device entry
    db_device = crud_device.get_device_by_device_id(db, device_id=device_id)
    if db_device is None:
        # Create a minimal device entry
        device_create = DeviceCreate(
            device_id=device_id,
            name=f"Device {device_id}",
            type="Unknown",
            manufacturer="Unknown",
            model="Unknown",
            serial_number=f"SN-{device_id}",
            installation_date=datetime.utcnow()
        )
        db_device = crud_device.create_device(db=db, device=device_create)
    
    # Check filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is missing")
    
    # Read file content
    content = await file.read()
    
    # Process based on file extension
    if file.filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    elif file.filename.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(io.BytesIO(content))
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV or Excel files.")
    
    # Convert DataFrame to DeviceData objects
    device_data_list = []
    for _, row in df.iterrows():
        # Map CSV columns to DeviceData fields
        # You may need to adjust these field names based on your CSV structure
        error_count_value = row.get('error_count')
        # Handle different types of error_count values
        if error_count_value is None or (isinstance(error_count_value, float) and pd.isna(error_count_value)):
            error_count = 0
        else:
            try:
                error_count = int(float(error_count_value))
            except (ValueError, TypeError):
                error_count = 0
        
        # Handle error_codes that might be NaN
        error_codes_value = row.get('error_codes')
        error_codes = str(error_codes_value) if error_codes_value is not None and not (isinstance(error_codes_value, float) and pd.isna(error_codes_value)) else None
        
        # Handle maintenance_notes that might be NaN
        maintenance_notes_value = row.get('maintenance_notes')
        maintenance_notes = str(maintenance_notes_value) if maintenance_notes_value is not None and not (isinstance(maintenance_notes_value, float) and pd.isna(maintenance_notes_value)) else None
        
        device_data = DeviceDataCreate(
            device_id=device_id,
            usage_hours=row.get('usage_hours'),
            temperature=row.get('temperature'),
            pressure=row.get('pressure'),
            vibration=row.get('vibration'),
            error_count=error_count,
            error_codes=error_codes,
            maintenance_notes=maintenance_notes
        )
        device_data_list.append(device_data)
    
    # Save to database
    created_data = crud_device_data.create_multiple_device_data(db, device_data_list)
    
    # Generate prediction for this device using the latest data
    try:
        # Get the latest device data for prediction
        latest_device_data = crud_device_data.get_device_data_by_device_id(db, device_id=device_id, limit=10)
        
        if latest_device_data:
            # Convert to DataFrame for ML model
            data_dicts = []
            for data in latest_device_data:
                data_dicts.append({
                    'usage_hours': data.usage_hours,
                    'temperature': data.temperature,
                    'pressure': data.pressure,
                    'vibration': data.vibration,
                    'error_count': data.error_count
                })
            
            df = pd.DataFrame(data_dicts)
            
            # Make prediction
            predictions = predictor.predict(df)
            # Use the first prediction (most recent data)
            predicted_status, confidence_score, recommendation = predictions[0]
            
            # Save prediction to database
            prediction_create = PredictionCreate(
                device_id=device_id,
                predicted_status=predicted_status,
                confidence_score=float(confidence_score),
                features_used=str(df.columns.tolist()),
                recommendation=recommendation
            )
            
            crud_prediction.create_prediction(db=db, prediction=prediction_create)
            
            return {"message": f"Successfully uploaded {len(created_data)} data points for device {device_id} and generated prediction"}
        else:
            return {"message": f"Successfully uploaded {len(created_data)} data points for device {device_id}. No data available for prediction."}
    except Exception as e:
        # Log the error but don't fail the upload
        print(f"Error generating prediction for device {device_id}: {str(e)}")
        return {"message": f"Successfully uploaded {len(created_data)} data points for device {device_id}. Failed to generate prediction: {str(e)}"}

@router.post("/bulk-upload-data")
async def bulk_upload_device_data(data: DeviceDataUpload, db: Session = Depends(get_db)):
    # Check if device exists, if not create a minimal device entry
    db_device = crud_device.get_device_by_device_id(db, device_id=data.device_id)
    if db_device is None:
        # Create a minimal device entry
        device_create = DeviceCreate(
            device_id=data.device_id,
            name=f"Device {data.device_id}",
            type="Unknown",
            manufacturer="Unknown",
            model="Unknown",
            serial_number=f"SN-{data.device_id}",
            installation_date=datetime.utcnow()
        )
        db_device = crud_device.create_device(db=db, device=device_create)
    
    # Save to database
    created_data = crud_device_data.create_multiple_device_data(db, data.data)
    
    return {"message": f"Successfully uploaded {len(created_data)} data points for device {data.device_id}"}