from fastapi import FastAPI, Depends, Request, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

# Import project components
from schemas import CustomerData, PredictionResult, PredictionHistoryBase
from database import get_db, Base, engine 
from crud import create_prediction_history, get_recent_history
from ml_model import predict_churn


Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


PUBLIC_USER_ID = 1 
def get_public_user():
    """Returns a placeholder user object for public access."""
    return {"id": PUBLIC_USER_ID, "username": "PublicUser", "role": "public"}



@app.post("/api/predict", response_model=PredictionResult)
def api_predict(
    customer_data: CustomerData, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_public_user) 
):
    """API endpoint to get a prediction and save history."""
    try:
        prediction = predict_churn(customer_data)
        
        
        history_data = PredictionHistoryBase(
            customer_id=current_user["id"],
            input_data=customer_data.dict(),
            timestamp=datetime.utcnow(), 
            **prediction.dict()
        )
        create_prediction_history(db, history_data)
        
        return prediction

    except Exception as e:
        print(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed due to server error. Check logs for: {str(e)}")

@app.get("/api/history")
def api_history(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_public_user) 
):
    """API endpoint to retrieve user-specific prediction history."""
    history = get_recent_history(db, limit=20) 
    return history



@app.get("/", name="dashboard_page")
def dashboard_page(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_public_user)):
    """Serves the main dashboard (now public)."""
    history_records = get_recent_history(db, limit=10)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "title": "Public Churn Prediction Dashboard",
        "username": current_user["username"],
        "history": history_records
    })

@app.get("/predict", name="predict_page")
def predict_page(request: Request, current_user: dict = Depends(get_public_user)):
    """Serves the prediction input page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "New Prediction",
        "username": current_user["username"]
    })

@app.get("/results", name="results_page")
def results_page(request: Request, db: Session = Depends(get_db), current_user: dict = Depends(get_public_user)):
    """Serves the final results page."""
    return templates.TemplateResponse("results.html", {"request": request})