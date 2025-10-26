from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas
from auth import get_password_hash 


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_prediction_history(db: Session, history: schemas.PredictionHistoryBase):
    
    db_history = models.PredictionHistory(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def get_recent_history(db: Session, user_id: Optional[int] = None, skip: int = 0, limit: int = 10):
    
    query = db.query(models.PredictionHistory).order_by(models.PredictionHistory.timestamp.desc())
    return query.offset(skip).limit(limit).all()