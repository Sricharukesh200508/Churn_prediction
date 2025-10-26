import pandas as pd
import numpy as np
import joblib 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier
import os


DATASET_PATH = 'churn.csv.csv'
OUTPUT_DIR = 'model_files'

try:
    df = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    print(f"Error: The file '{DATASET_PATH}' was not found. Please place it in the root directory.")
    exit()

df.replace(' ', np.nan, inplace=True)
df.dropna(inplace=True)
df.drop('customerID', axis=1, inplace=True)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
df['Churn'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)


X = df.drop('Churn', axis=1)
y = df['Churn']


numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
categorical_features = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
    'Contract', 'PaperlessBilling', 'PaymentMethod'
]


preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = XGBClassifier(
    objective='binary:logistic',
    eval_metric='logloss',
    use_label_encoder=False,
    random_state=42,
    scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train)
)

print("Training XGBoost model...")
model.fit(preprocessor.fit_transform(X_train), y_train)
print("Model trained successfully.")


os.makedirs(OUTPUT_DIR, exist_ok=True)
joblib.dump(model, os.path.join(OUTPUT_DIR, 'model.pkl'))
joblib.dump(preprocessor, os.path.join(OUTPUT_DIR, 'preprocessor.pkl'))

print(f"Model and preprocessor saved to the '{OUTPUT_DIR}' directory.")