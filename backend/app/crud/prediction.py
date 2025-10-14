from sqlalchemy.orm import Session
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate, PredictionUpdate
from datetime import datetime

def get_prediction(db: Session, prediction_id: int):
    return db.query(Prediction).filter(Prediction.id == prediction_id).first()

def get_predictions_by_device_id(db: Session, device_id: str, skip: int = 0, limit: int = 100):
    return db.query(Prediction).filter(Prediction.device_id == device_id).offset(skip).limit(limit).all()

def get_recent_predictions(db: Session, hours: int = 24):
    # This would need to be adjusted based on your needs
    return db.query(Prediction).limit(100).all()

def create_prediction(db: Session, prediction: PredictionCreate):
    db_prediction = Prediction(**prediction.dict())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def create_multiple_predictions(db: Session, predictions: list):
    db_predictions = []
    for pred in predictions:
        db_prediction = Prediction(**pred.dict())
        db_predictions.append(db_prediction)
    
    db.add_all(db_predictions)
    db.commit()
    for db_prediction in db_predictions:
        db.refresh(db_prediction)
    return db_predictions

def update_prediction(db: Session, prediction_id: int, prediction_update: PredictionUpdate):
    db_prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if db_prediction:
        update_data = prediction_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_prediction, key, value)
        db.commit()
        db.refresh(db_prediction)
    return db_prediction

def delete_prediction(db: Session, prediction_id: int):
    db_prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if db_prediction:
        db.delete(db_prediction)
        db.commit()
    return db_prediction