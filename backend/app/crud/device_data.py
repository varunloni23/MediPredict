from sqlalchemy.orm import Session
from app.models.device_data import DeviceData
from app.schemas.device_data import DeviceDataCreate, DeviceDataUpdate
from datetime import datetime

def get_device_data(db: Session, data_id: int):
    return db.query(DeviceData).filter(DeviceData.id == data_id).first()

def get_device_data_by_device_id(db: Session, device_id: str, skip: int = 0, limit: int = 100):
    return db.query(DeviceData).filter(DeviceData.device_id == device_id).offset(skip).limit(limit).all()

def get_all_device_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeviceData).offset(skip).limit(limit).all()

def create_device_data(db: Session, device_data: DeviceDataCreate):
    # If timestamp is not provided, use current time
    if not device_data.timestamp:
        device_data.timestamp = datetime.utcnow()
    
    db_device_data = DeviceData(**device_data.dict())
    db.add(db_device_data)
    db.commit()
    db.refresh(db_device_data)
    return db_device_data

def create_multiple_device_data(db: Session, device_data_list: list):
    db_device_data_list = []
    for data in device_data_list:
        if not data.timestamp:
            data.timestamp = datetime.utcnow()
        db_device_data = DeviceData(**data.dict())
        db_device_data_list.append(db_device_data)
    
    db.add_all(db_device_data_list)
    db.commit()
    for db_device_data in db_device_data_list:
        db.refresh(db_device_data)
    return db_device_data_list

def update_device_data(db: Session, data_id: int, device_data_update: DeviceDataUpdate):
    db_device_data = db.query(DeviceData).filter(DeviceData.id == data_id).first()
    if db_device_data:
        update_data = device_data_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_device_data, key, value)
        db.commit()
        db.refresh(db_device_data)
    return db_device_data

def delete_device_data(db: Session, data_id: int):
    db_device_data = db.query(DeviceData).filter(DeviceData.id == data_id).first()
    if db_device_data:
        db.delete(db_device_data)
        db.commit()
    return db_device_data