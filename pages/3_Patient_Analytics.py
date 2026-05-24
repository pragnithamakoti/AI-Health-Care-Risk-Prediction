import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from utils.auth import require_auth
from utils.ui_components import apply_custom_css

st.set_page_config(page_title="Analytics | Nexus AI", layout="wide", initial_sidebar_state="expanded")
apply_custom_css()
require_auth(['Admin', 'Doctor', 'Analyst'])

st.markdown("<h1>📈 Patient <span class='neon-text'>Analytics</span></h1>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets', 'healthcare_dataset.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df = load_data()

if df is None:
    st.error("Dataset not found.")
    st.stop()

# Filters
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("### 🔍 Global Filters")
col1, col2, col3 = st.columns(3)
with col1:
    disease_filter = st.multiselect("Disease Category", options=df['Disease_Label'].unique(), default=df['Disease_Label'].unique())
with col2:
    gender_filter = st.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
with col3:
    age_range = st.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), (20, 80))
st.markdown("</div>", unsafe_allow_html=True)

filtered_df = df[
    (df['Disease_Label'].isin(disease_filter)) &
    (df['Gender'].isin(gender_filter)) &
    (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])
]

# Row 1: Demographics
c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Age Distribution by Risk")
    fig = px.histogram(filtered_df, x="Age", color="Disease_Label", marginal="box", 
                       color_discrete_sequence=['#00F3FF', '#0057FF', '#10B981', '#F59E0B', '#EF4444'],
                       nbins=30)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
with c2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Cholesterol vs Glucose (Risk Segmentation)")
    fig2 = px.scatter(filtered_df, x="Glucose", y="Cholesterol", color="Disease_Label", size="BMI", opacity=0.7,
                      color_discrete_sequence=['#00F3FF', '#0057FF', '#10B981', '#F59E0B', '#EF4444'])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Row 2: Lifestyle Impact
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("### Lifestyle Impact Analysis")
c3, c4 = st.columns(2)
with c3:
    st.markdown("#### Smoking vs Disease Rate")
    smoking_ct = pd.crosstab(filtered_df['Smoking_Habit'], filtered_df['Disease_Label'], normalize='index') * 100
    smoking_ct = smoking_ct.reset_index()
    fig3 = px.bar(smoking_ct, x="Smoking_Habit", y=smoking_ct.columns[1:], barmode='stack',
                  color_discrete_sequence=['#00F3FF', '#0057FF', '#10B981', '#F59E0B', '#EF4444'])
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'), yaxis_title="Percentage (%)")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.markdown("#### Stress Level Correlation")
    stress_ct = pd.crosstab(filtered_df['Stress_Level'], filtered_df['Disease_Label'], normalize='index') * 100
    stress_ct = stress_ct.reset_index()
    fig4 = px.bar(stress_ct, x="Stress_Level", y=stress_ct.columns[1:], barmode='stack',
                  color_discrete_sequence=['#00F3FF', '#0057FF', '#10B981', '#F59E0B', '#EF4444'])
    fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'), yaxis_title="Percentage (%)")
    st.plotly_chart(fig4, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
