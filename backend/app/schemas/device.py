from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    device_id: str
    name: str
    type: str
    manufacturer: str
    model: str
    serial_number: str
    installation_date: datetime
    last_maintenance_date: Optional[datetime] = None
    status: Optional[str] = "active"

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    last_maintenance_date: Optional[datetime] = None
    status: Optional[str] = None

class Device(DeviceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True