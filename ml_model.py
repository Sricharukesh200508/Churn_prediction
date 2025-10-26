import joblib
import pandas as pd
import shap
from typing import Dict, Any, List
import os
import numpy as np
from schemas import CustomerData, PredictionResult


MODEL_PATH = os.path.join(os.getcwd(), 'model_files/model.pkl')
PREPROCESSOR_PATH = os.path.join(os.getcwd(), 'model_files/preprocessor.pkl')

model = None
preprocessor = None
explainer = None

def load_ml_assets():
    """Loads the trained ML model, preprocessor, and sets up SHAP explainer."""
    global model, preprocessor, explainer
    try:
        model = joblib.load(MODEL_PATH)
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        
        explainer = shap.TreeExplainer(model)
        print("SHAP TreeExplainer initialized.")
    except FileNotFoundError:
        print(f"Error: Model files not found. Run train_model.py first.")
        raise
    except Exception as e:
        print(f"Error loading ML assets: {e}")
        raise


def get_feature_names_out(preprocessor):
    return preprocessor.get_feature_names_out()


def predict_churn(customer_data: CustomerData) -> PredictionResult:
    """
    Runs the model and calculates SHAP contributions.
    """
    global model, preprocessor, explainer
    if model is None or preprocessor is None:
        load_ml_assets()

    if explainer is None:
        raise RuntimeError("SHAP Explainer not initialized.")
    
    input_df = pd.DataFrame([customer_data.dict()])
    processed_data = preprocessor.transform(input_df)

    
    churn_probability = model.predict_proba(processed_data)[:, 1][0]
    churn_prediction_raw = model.predict(processed_data)[0]

    
    shap_values = explainer.shap_values(processed_data)[0]
    feature_names = get_feature_names_out(preprocessor)
    contributions = {
        name: float(value) 
        for name, value in zip(feature_names, shap_values)
    }

    
    result = PredictionResult(
        churn_probability=float(churn_probability),
        churn_prediction=bool(churn_prediction_raw),
        feature_contributions=contributions
    )

    return result