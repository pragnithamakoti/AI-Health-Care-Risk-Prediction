import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import time
from utils.auth import require_auth
from utils.ui_components import apply_custom_css, render_alert

st.set_page_config(page_title="AI Prediction | Nexus AI", layout="wide", initial_sidebar_state="expanded")
apply_custom_css()
require_auth(['Admin', 'Doctor'])

st.markdown("<h1>🧠 AI Risk <span class='neon-text'>Prediction</span> Engine</h1>", unsafe_allow_html=True)
st.markdown("Enter patient vitals below to generate a comprehensive risk analysis using our XGBoost and Random Forest models.")

@st.cache_resource
def load_pipeline():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'ai_models_pipeline.pkl')
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return None

pipeline = load_pipeline()

if pipeline is None:
    st.error("ML Models not found. Please train models first.")
    st.stop()

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Patient Vitals")
    
    with st.form("prediction_form"):
        age = st.slider("Age", 18, 100, 45)
        gender = st.selectbox("Gender", ["Male", "Female"])
        
        c1, c2 = st.columns(2)
        height = c1.number_input("Height (cm)", 100.0, 250.0, 170.0)
        weight = c2.number_input("Weight (kg)", 30.0, 200.0, 75.0)
        bmi = weight / ((height/100)**2)
        
        c3, c4 = st.columns(2)
        sys_bp = c3.number_input("Systolic BP", 80, 200, 120)
        dia_bp = c4.number_input("Diastolic BP", 50, 130, 80)
        
        c5, c6 = st.columns(2)
        cholesterol = c5.number_input("Cholesterol", 100.0, 400.0, 180.0)
        glucose = c6.number_input("Glucose", 50.0, 300.0, 90.0)
        
        st.markdown("### Lifestyle & History")
        c7, c8 = st.columns(2)
        smoking = c7.selectbox("Smoking Habit", ["Never", "Occasional", "Regular"])
        alcohol = c8.selectbox("Alcohol Consumption", ["Never", "Occasional", "Regular"])
        
        c9, c10 = st.columns(2)
        activity = c9.selectbox("Physical Activity", ["Low", "Moderate", "High"])
        stress = c10.selectbox("Stress Level", ["Low", "Medium", "High"])
        
        family_hist = st.selectbox("Family History of Major Diseases", ["No", "Yes"])
        
        submitted = st.form_submit_button("Run AI Analysis")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Prediction Results")
    
    if submitted:
        with st.spinner("Analyzing patient matrix..."):
            time.sleep(1.5) # UX delay
            
            # Prepare Input
            input_data = pd.DataFrame([{
                'Age': age, 'BMI': bmi, 'Systolic_BP': sys_bp, 'Diastolic_BP': dia_bp,
                'Cholesterol': cholesterol, 'Glucose': glucose, 'Gender': gender,
                'Smoking_Habit': smoking, 'Alcohol_Consumption': alcohol,
                'Physical_Activity': activity, 'Stress_Level': stress,
                'Family_History': family_hist
            }])
            
            # Encode Categorical
            for col, le in pipeline['label_encoders'].items():
                input_data[col] = le.transform(input_data[col])
                
            # Scale
            input_scaled = pipeline['scaler'].transform(input_data)
            
            # Predict (Using XGBoost as primary)
            xgb_model = pipeline['xgb_model']
            pred_class = xgb_model.predict(input_scaled)[0]
            pred_probs = xgb_model.predict_proba(input_scaled)[0]
            
            target_le = pipeline['target_encoder']
            disease_label = target_le.inverse_transform([pred_class])[0]
            
            # Display Result
            if disease_label == "Healthy":
                st.markdown(f"<h2 style='text-align: center; color: #10B981;'>No Major Risks Detected</h2>", unsafe_allow_html=True)
                render_alert("Patient vitals are within normal ranges. Encourage maintaining current lifestyle.", "success")
            else:
                st.markdown(f"<h2 style='text-align: center; color: #EF4444;'>High Risk: {disease_label}</h2>", unsafe_allow_html=True)
                render_alert(f"Immediate attention recommended. AI confidence: {max(pred_probs)*100:.1f}%", "danger")
                
            st.markdown("#### Probability Distribution")
            classes = target_le.classes_
            
            for cls, prob in zip(classes, pred_probs):
                color = "#EF4444" if prob > 0.5 else "#F59E0B" if prob > 0.2 else "#10B981"
                st.markdown(f"**{cls}**: {prob*100:.1f}%")
                st.markdown(
                    f"""
                    <div style="width: 100%; background-color: #1E293B; border-radius: 4px; margin-bottom: 15px;">
                      <div style="width: {prob*100}%; height: 8px; background-color: {color}; border-radius: 4px;"></div>
                    </div>
                    """, unsafe_allow_html=True
                )
                
            st.markdown("#### AI Recommendations")
            if "Heart" in disease_label or "Hypertension" in disease_label:
                st.write("🩺 Consult a cardiologist. Monitor BP daily.")
            if "Diabetes" in disease_label:
                st.write("🩺 Schedule an HbA1c test. Advise low-carb diet.")
            if "Lung" in disease_label or smoking == "Regular":
                st.write("🩺 Recommend smoking cessation program and spirometry test.")
                
            st.button("Save Report to Patient Profile (Simulated)", key="save_rep")
            
    else:
        st.info("Awaiting patient data. Fill the form on the left to generate insights.")
        
    st.markdown("</div>", unsafe_allow_html=True)
