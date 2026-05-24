# AI Healthcare Risk Prediction System

A complete professional AI-powered healthcare analytics system built with Python, Streamlit, and Machine Learning. The platform features predictive models for various health risks, interactive visual analytics, and a premium dark UI designed for enterprise-level medical intelligence.

## Features

- **Predictive Analytics:** Machine learning models (Random Forest, XGBoost, Logistic Regression) predicting risks for Heart Disease, Diabetes, Lung Disease, and Hypertension.
- **Role-Based Access Control:** Secure authentication for Admin, Doctor, and Analyst roles.
- **Real-Time Dashboards:** Interactive Plotly visualizations for patient demographics, lifestyle impact, and disease trends.
- **Admin Panel:** Complete management of users, prediction history, and system logs.
- **Premium UI:** Dark theme, neon highlights, glassmorphism effects, and fully responsive layout.
- **Power BI Blueprint:** Comprehensive guide for building an enterprise-grade Power BI dashboard complementing this system.

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Synthetic Dataset & Train Models:**
   First, run the data generator and the model training scripts to populate the `datasets/` and `models/` directories.
   ```bash
   python utils/data_generator.py
   python utils/train_models.py
   ```

3. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

## Default Accounts
- **Admin**: admin (password: admin123)
- **Doctor**: doctor (password: doctor123)
- **Analyst**: analyst (password: analyst123)
