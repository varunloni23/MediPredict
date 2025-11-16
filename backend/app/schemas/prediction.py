from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PredictionBase(BaseModel):
    device_id: str
    predicted_status: str
    confidence_score: float
    features_used: str
    recommendation: Optional[str] = None

class PredictionCreate(PredictionBase):
    pass

class PredictionUpdate(PredictionBase):
    pass

class Prediction(PredictionBase):
    id: int
    prediction_timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class PredictionResult(PredictionBase):
    id: int
    prediction_timestamp: datetime
    
class BulkPredictionRequest(BaseModel):
    device_ids: List[str]