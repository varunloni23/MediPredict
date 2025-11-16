from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"))
    prediction_timestamp = Column(DateTime, default=datetime.utcnow)
    predicted_status = Column(String)  # healthy, at_risk, needs_maintenance
    confidence_score = Column(Float)
    features_used = Column(String)  # JSON string of features used for prediction
    recommendation = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Prediction(device_id='{self.device_id}', status='{self.predicted_status}')>"