from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.database import Base
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    manufacturer = Column(String)
    model = Column(String)
    serial_number = Column(String, unique=True)
    installation_date = Column(DateTime)
    last_maintenance_date = Column(DateTime, nullable=True)
    status = Column(String, default="active")  # active, inactive, maintenance
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Device(name='{self.name}', device_id='{self.device_id}')>"