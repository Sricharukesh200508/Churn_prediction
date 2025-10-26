# Churn_prediction
# 🧠 Customer Churn Prediction API

This project is a **Machine Learning Web App** that predicts customer churn — i.e., whether a telecom customer is likely to leave the service — based on demographic, usage, and billing data.

It is built using **FastAPI**, trained with **Logistic Regression**, and designed for deployment on **Google Cloud Vertex AI** or any cloud platform.

---

## 🚀 Features

- Predict customer churn probability using a trained ML model
- RESTful API built with **FastAPI**
- Preprocessing pipeline using **Scikit-learn ColumnTransformer**
- Model trained using **Logistic Regression**
- Supports cloud-native deployment (Vertex AI / Docker)
- Includes all artifacts: `model.pkl`, `preprocessor.pkl`, `requirements.txt`

---

## 🧩 Tech Stack

- **Python 3.12**
- **FastAPI** (Web Framework)
- **Scikit-learn** (Model + Preprocessing)
- **Pandas & NumPy** (Data Processing)
- **Joblib** (Model Serialization)
- **Uvicorn** (Server)
- **Docker** (Containerization)
- **Google Cloud Vertex AI** (Deployment)

---

## 🧠 Model Training

The model was trained using the **Telco Customer Churn Dataset**.  
Steps include:
1. Data cleaning and preprocessing
2. Encoding categorical and numeric features
3. Model training with Logistic Regression
4. Saving trained model and preprocessor with `joblib`

To retrain:
```bash
python train_model.py

model.pkl – trained Logistic Regression model
preprocessor.pkl – feature transformation pipeline

git clone https://github.com/Sricharukesh200508/Churn_prediction.git
cd Churn_prediction

Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
then visit:
http://0.0.0.0:8080
