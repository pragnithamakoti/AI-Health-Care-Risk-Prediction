import streamlit as st
import pandas as pd
import os
import plotly.express as px
from utils.auth import require_auth
from utils.ui_components import apply_custom_css, render_kpi_card

st.set_page_config(page_title="Dashboard | Nexus AI", layout="wide", initial_sidebar_state="expanded")
apply_custom_css()
require_auth(['Admin', 'Doctor', 'Analyst'])

st.markdown("<h1>📊 Executive <span class='neon-text'>Overview</span></h1>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets', 'healthcare_dataset.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df = load_data()

if df is not None:
    # Calculate KPIs
    total_patients = len(df)
    high_risk_patients = len(df[df['Disease_Label'] != 'Healthy'])
    avg_bmi = df['BMI'].mean()
    smoking_pct = (len(df[df['Smoking_Habit'] == 'Regular']) / total_patients) * 100
    
    # Render KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Patients", f"{total_patients:,}", "+124 this month", "up")
    with col2:
        render_kpi_card("High Risk Cases", f"{high_risk_patients:,}", f"{(high_risk_patients/total_patients)*100:.1f}% of total", "down")
    with col3:
        render_kpi_card("Average BMI", f"{avg_bmi:.1f}", "-0.5 from avg", "up")
    with col4:
        render_kpi_card("Regular Smokers", f"{smoking_pct:.1f}%", "+2.1% warning", "down")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Disease Distribution")
        disease_counts = df['Disease_Label'].value_counts().reset_index()
        disease_counts.columns = ['Disease', 'Count']
        fig = px.pie(disease_counts, values='Count', names='Disease', hole=0.7, 
                     color_discrete_sequence=['#00F3FF', '#0057FF', '#10B981', '#F59E0B', '#EF4444'])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0'), margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with chart_col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Age vs BMI Distribution")
        fig2 = px.scatter(df, x='Age', y='BMI', color='Disease_Label', opacity=0.6,
                          color_discrete_sequence=['#00F3FF', '#0057FF', '#10B981', '#F59E0B', '#EF4444'])
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E2E8F0'), margin=dict(t=30, b=0, l=0, r=0),
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("Dataset not found. Please run the data generator first.")
