from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from datetime import datetime, timedelta
from app.database import get_db
from app.crud import device as crud_device, prediction as crud_prediction, device_data as crud_device_data
from app.schemas.device import Device
from app.schemas.prediction import Prediction

router = APIRouter()

@router.get("/export-devices")
def export_devices_csv(db: Session = Depends(get_db)):
    """
    Export all devices as CSV
    """
    try:
        # Get all devices
        devices = crud_device.get_devices(db, skip=0, limit=1000)
        
        # Convert to DataFrame
        data = []
        for device in devices:
            data.append({
                'device_id': device.device_id,
                'name': device.name,
                'type': device.type,
                'manufacturer': device.manufacturer,
                'model': device.model,
                'serial_number': device.serial_number,
                'installation_date': device.installation_date,
                'last_maintenance_date': device.last_maintenance_date,
                'status': device.status
            })
        
        df = pd.DataFrame(data)
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Return as downloadable CSV
        headers = {
            'Content-Disposition': 'attachment; filename="devices_report.csv"',
            'Content-Type': 'text/csv'
        }
        return Response(content=csv_data, headers=headers)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export devices: {str(e)}")

@router.get("/export-predictions")
def export_predictions_csv(db: Session = Depends(get_db)):
    """
    Export all predictions as CSV
    """
    try:
        # Get recent predictions
        predictions = crud_prediction.get_recent_predictions(db)
        
        # Convert to DataFrame
        data = []
        for pred in predictions:
            data.append({
                'device_id': pred.device_id,
                'predicted_status': pred.predicted_status,
                'confidence_score': pred.confidence_score,
                'recommendation': pred.recommendation,
                'prediction_timestamp': pred.prediction_timestamp
            })
        
        df = pd.DataFrame(data)
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Return as downloadable CSV
        headers = {
            'Content-Disposition': 'attachment; filename="predictions_report.csv"',
            'Content-Type': 'text/csv'
        }
        return Response(content=csv_data, headers=headers)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export predictions: {str(e)}")

@router.get("/export-device-data/{device_id}")
def export_device_data_csv(device_id: str, db: Session = Depends(get_db)):
    """
    Export device data points as CSV
    """
    try:
        # Get device data
        device_data_list = crud_device_data.get_device_data_by_device_id(db, device_id=device_id, limit=1000)
        
        if not device_data_list:
            raise HTTPException(status_code=404, detail="No data found for this device")
        
        # Convert to DataFrame
        data = []
        for data_point in device_data_list:
            data.append({
                'device_id': data_point.device_id,
                'timestamp': data_point.timestamp,
                'usage_hours': data_point.usage_hours,
                'temperature': data_point.temperature,
                'pressure': data_point.pressure,
                'vibration': data_point.vibration,
                'error_count': data_point.error_count,
                'error_codes': data_point.error_codes,
                'maintenance_notes': data_point.maintenance_notes
            })
        
        df = pd.DataFrame(data)
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Return as downloadable CSV
        headers = {
            'Content-Disposition': f'attachment; filename="device_data_{device_id}_report.csv"',
            'Content-Type': 'text/csv'
        }
        return Response(content=csv_data, headers=headers)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export device data: {str(e)}")

@router.get("/summary-report")
def get_summary_report(db: Session = Depends(get_db)):
    """
    Get a summary report of device health status
    """
    try:
        # Get all devices
        devices = crud_device.get_devices(db, skip=0, limit=1000)
        
        # Get recent predictions
        predictions = crud_prediction.get_recent_predictions(db)
        
        # Create a mapping of device_id to latest prediction
        prediction_map = {}
        for pred in predictions:
            if pred.device_id not in prediction_map:
                prediction_map[pred.device_id] = pred
        
        # Count device statuses
        status_counts = {'healthy': 0, 'at_risk': 0, 'needs_maintenance': 0, 'unknown': 0}
        for device in devices:
            if device.device_id in prediction_map:
                status = prediction_map[device.device_id].predicted_status
                status_counts[status] = status_counts.get(status, 0) + 1
            else:
                status_counts['unknown'] = status_counts['unknown'] + 1
        
        # Return summary data
        return {
            "total_devices": len(devices),
            "status_breakdown": status_counts,
            "report_generated": datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary report: {str(e)}")