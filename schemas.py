from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int
    is_active: bool = True
    role: str = "user"

    class Config:
        orm_mode = True


class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


class PredictionResult(BaseModel):
    churn_probability: float = Field(..., ge=0.0, le=1.0)
    churn_prediction: bool
    feature_contributions: Dict[str, float] 

class PredictionHistoryBase(PredictionResult):
    customer_id: int
    timestamp: datetime
    input_data: Dict

class PredictionHistory(PredictionHistoryBase):
    id: int
    
    class Config:
        orm_mode = True