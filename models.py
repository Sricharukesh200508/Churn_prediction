from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, JSON
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    id = Column(Integer, primary_key=True, index=True)
    churn_probability = Column(Float, nullable=False)
    churn_prediction = Column(Boolean, nullable=False)
    customer_id = Column(Integer, index=True) 
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_data = Column(JSON)
    feature_contributions = Column(JSON)