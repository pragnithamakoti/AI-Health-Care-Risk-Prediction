import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def train_and_save_models():
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets', 'healthcare_dataset.csv')
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return
        
    df = pd.read_csv(dataset_path)
    
    # Feature Engineering / Selection
    features = [
        'Age', 'BMI', 'Systolic_BP', 'Diastolic_BP', 'Cholesterol', 'Glucose',
        'Gender', 'Smoking_Habit', 'Alcohol_Consumption', 'Physical_Activity',
        'Stress_Level', 'Family_History'
    ]
    
    X = df[features].copy()
    y = df['Disease_Label']
    
    # Label Encoding for categorical features
    label_encoders = {}
    categorical_cols = ['Gender', 'Smoking_Habit', 'Alcohol_Consumption', 'Physical_Activity', 'Stress_Level', 'Family_History']
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
        
    # Target Encoding
    target_le = LabelEncoder()
    y_encoded = target_le.fit_transform(y)
    
    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training Models...")
    
    # 1. Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    rf_pred = rf_model.predict(X_test_scaled)
    print(f"Random Forest Accuracy: {accuracy_score(y_test, rf_pred):.4f}")
    
    # 2. XGBoost
    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    xgb_model.fit(X_train_scaled, y_train)
    xgb_pred = xgb_model.predict(X_test_scaled)
    print(f"XGBoost Accuracy: {accuracy_score(y_test, xgb_pred):.4f}")
    
    # 3. Logistic Regression
    lr_model = LogisticRegression(max_iter=1000, multi_class='multinomial')
    lr_model.fit(X_train_scaled, y_train)
    lr_pred = lr_model.predict(X_test_scaled)
    print(f"Logistic Regression Accuracy: {accuracy_score(y_test, lr_pred):.4f}")
    
    # Save artifacts
    artifacts = {
        'rf_model': rf_model,
        'xgb_model': xgb_model,
        'lr_model': lr_model,
        'scaler': scaler,
        'label_encoders': label_encoders,
        'target_encoder': target_le,
        'feature_names': features
    }
    
    with open(os.path.join(models_dir, 'ai_models_pipeline.pkl'), 'wb') as f:
        pickle.dump(artifacts, f)
        
    print("Models and preprocessors saved to models/ai_models_pipeline.pkl")

if __name__ == "__main__":
    train_and_save_models()
