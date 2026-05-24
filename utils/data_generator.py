import pandas as pd
import numpy as np
import os

def generate_healthcare_data(num_samples=5000):
    np.random.seed(42)
    
    # Basic Demographics
    age = np.random.randint(18, 90, num_samples)
    gender = np.random.choice(['Male', 'Female'], num_samples, p=[0.48, 0.52])
    
    # Vitals
    height_cm = np.random.normal(170, 10, num_samples)
    weight_kg = np.random.normal(75, 15, num_samples)
    bmi = weight_kg / ((height_cm/100)**2)
    
    # Clinical
    sys_bp = np.random.normal(120, 15, num_samples) + (age * 0.1)
    dia_bp = np.random.normal(80, 10, num_samples) + (age * 0.05)
    blood_pressure = [f"{int(s)}/{int(d)}" for s, d in zip(sys_bp, dia_bp)]
    
    cholesterol = np.random.normal(180, 30, num_samples) + (bmi * 1.5) + (age * 0.5)
    glucose = np.random.normal(90, 20, num_samples) + (bmi * 1.2) + (age * 0.2)
    
    # Lifestyle
    smoking_habit = np.random.choice(['Never', 'Occasional', 'Regular'], num_samples, p=[0.6, 0.2, 0.2])
    alcohol_consumption = np.random.choice(['Never', 'Occasional', 'Regular'], num_samples, p=[0.5, 0.3, 0.2])
    physical_activity = np.random.choice(['Low', 'Moderate', 'High'], num_samples, p=[0.3, 0.5, 0.2])
    sleep_hours = np.random.normal(7, 1.5, num_samples)
    stress_level = np.random.choice(['Low', 'Medium', 'High'], num_samples, p=[0.3, 0.4, 0.3])
    
    # History
    family_history = np.random.choice(['Yes', 'No'], num_samples, p=[0.3, 0.7])
    
    # Introduce Correlated Risks based on features
    heart_risk_score = (age/100) * 0.3 + (bmi/50) * 0.2 + (cholesterol/300) * 0.3 + (np.where(np.array(smoking_habit) == 'Regular', 0.2, 0))
    diabetes_risk_score = (bmi/50) * 0.4 + (glucose/200) * 0.4 + (np.where(np.array(family_history) == 'Yes', 0.2, 0))
    lung_risk_score = (np.where(np.array(smoking_habit) == 'Regular', 0.6, 0)) + (age/100) * 0.4
    hypertension_risk_score = (sys_bp/200) * 0.5 + (stress_level == 'High') * 0.2 + (bmi/50) * 0.3
    
    # Labels
    disease_label = []
    for h, d, l, hyp in zip(heart_risk_score, diabetes_risk_score, lung_risk_score, hypertension_risk_score):
        max_score = max(h, d, l, hyp)
        if max_score > 0.65:
            if max_score == h:
                disease_label.append("Heart Disease")
            elif max_score == d:
                disease_label.append("Diabetes")
            elif max_score == l:
                disease_label.append("Lung Disease")
            else:
                disease_label.append("Hypertension")
        else:
            disease_label.append("Healthy")
            
    df = pd.DataFrame({
        'Age': age,
        'Gender': gender,
        'Height': np.round(height_cm, 1),
        'Weight': np.round(weight_kg, 1),
        'BMI': np.round(bmi, 1),
        'Blood_Pressure': blood_pressure,
        'Systolic_BP': np.round(sys_bp, 0),
        'Diastolic_BP': np.round(dia_bp, 0),
        'Cholesterol': np.round(cholesterol, 1),
        'Glucose': np.round(glucose, 1),
        'Smoking_Habit': smoking_habit,
        'Alcohol_Consumption': alcohol_consumption,
        'Physical_Activity': physical_activity,
        'Sleep_Hours': np.round(sleep_hours, 1),
        'Stress_Level': stress_level,
        'Family_History': family_history,
        'Disease_Label': disease_label
    })
    
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets', 'healthcare_dataset.csv')
    df.to_csv(dataset_path, index=False)
    print(f"Dataset generated and saved to {dataset_path} with {num_samples} records.")
    return df

if __name__ == "__main__":
    generate_healthcare_data(10000)
