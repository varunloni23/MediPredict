from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from app.database import Base
from datetime import datetime

class DeviceData(Base):
    __tablename__ = "device_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    usage_hours = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    vibration = Column(Float, nullable=True)
    error_count = Column(Integer, default=0)
    error_codes = Column(Text, nullable=True)  # JSON string of error codes
    maintenance_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<DeviceData(device_id='{self.device_id}', timestamp='{self.timestamp}')>"