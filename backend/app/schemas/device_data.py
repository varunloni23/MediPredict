from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DeviceDataBase(BaseModel):
    device_id: str
    usage_hours: Optional[float] = None
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    vibration: Optional[float] = None
    error_count: int = 0
    error_codes: Optional[str] = None
    maintenance_notes: Optional[str] = None

class DeviceDataCreate(DeviceDataBase):
    timestamp: Optional[datetime] = None

class DeviceDataUpdate(DeviceDataBase):
    pass

class DeviceData(DeviceDataBase):
    id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class DeviceDataUpload(BaseModel):
    device_id: str
    data: List[DeviceDataCreate]