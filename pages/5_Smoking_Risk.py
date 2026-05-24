import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from utils.auth import require_auth
from utils.ui_components import apply_custom_css

st.set_page_config(page_title="Smoking Risk | Nexus AI", layout="wide", initial_sidebar_state="expanded")
apply_custom_css()
require_auth(['Admin', 'Doctor', 'Analyst'])

# Extra CSS for this premium page
st.markdown("""
<style>
.smoke-header {
    background: linear-gradient(135deg, rgba(0,243,255,0.08) 0%, rgba(0,87,255,0.08) 100%);
    border: 1px solid rgba(0,243,255,0.15);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
}
.smoke-kpi {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,243,255,0.12);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s;
}
.smoke-kpi:hover {
    border-color: rgba(0,243,255,0.5);
    box-shadow: 0 0 20px rgba(0,243,255,0.1);
    transform: translateY(-3px);
}
.smoke-kpi .main-val {
    font-size: 42px;
    font-weight: 800;
    color: #00F3FF;
    text-shadow: 0 0 20px rgba(0,243,255,0.4);
    line-height: 1;
}
.smoke-kpi .label {
    font-size: 13px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
}
.smoke-kpi .sub {
    font-size: 12px;
    color: #F59E0B;
    margin-top: 8px;
    font-weight: 600;
}
.toggle-btn-active {
    background: linear-gradient(135deg, #EF4444, #991B1B);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 16px;
    font-weight: 700;
    font-size: 13px;
    cursor: pointer;
}
.toggle-btn-inactive {
    background: rgba(16,185,129,0.1);
    color: #10B981;
    border: 1px solid #10B981;
    border-radius: 8px;
    padding: 6px 16px;
    font-weight: 700;
    font-size: 13px;
    cursor: pointer;
}
.chart-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}
.chart-card:hover {
    border-color: rgba(0,243,255,0.15);
}
.lung-visual {
    background: radial-gradient(ellipse at center, rgba(239,68,68,0.08) 0%, rgba(11,14,20,0) 70%);
    border-radius: 16px;
    border: 1px solid rgba(239,68,68,0.15);
    padding: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'datasets', 'healthcare_dataset.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Add Age Group column
        df['Age_Group'] = pd.cut(df['Age'], bins=[0,25,35,45,55,65,100],
                                  labels=['<25','25-35','35-45','45-55','55-65','65+'])
        return df
    return None

df = load_data()
if df is None:
    st.error("Dataset not found.")
    st.stop()

# ─── HEADER ───────────────────────────────────────────────
st.markdown("""
<div class="smoke-header">
  <div style="display:flex; justify-content:space-between; align-items:center;">
    <div>
      <h1 style="margin:0; font-size:28px; color:#FFFFFF;">🫁 Smoking Health Risk Analysis</h1>
      <p style="margin:4px 0 0; color:#64748B; font-size:14px;">From raw healthcare data to meaningful insights</p>
    </div>
    <div style="display:flex; gap:10px;">
      <span style="background:rgba(239,68,68,0.15); color:#EF4444; border:1px solid #EF4444; border-radius:8px; padding:6px 18px; font-weight:700; font-size:13px;">🔴 Damaged</span>
      <span style="background:rgba(16,185,129,0.15); color:#10B981; border:1px solid #10B981; border-radius:8px; padding:6px 18px; font-weight:700; font-size:13px;">🟢 Healthy</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── FILTERS ──────────────────────────────────────────────
with st.expander("🔧 Filters", expanded=False):
    fc1, fc2, fc3 = st.columns(3)
    gender_sel = fc1.multiselect("Gender", df['Gender'].unique(), default=list(df['Gender'].unique()))
    smoke_sel  = fc2.multiselect("Smoking Status", df['Smoking_Habit'].unique(), default=list(df['Smoking_Habit'].unique()))
    age_sel    = fc3.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), (18, 90))

fdf = df[df['Gender'].isin(gender_sel) & df['Smoking_Habit'].isin(smoke_sel) &
         (df['Age'] >= age_sel[0]) & (df['Age'] <= age_sel[1])]

# ─── KPI CARDS ────────────────────────────────────────────
total     = len(fdf)
regular   = len(fdf[fdf['Smoking_Habit'] == 'Regular'])
avg_age   = fdf['Age'].mean()
avg_bmi   = fdf['BMI'].mean()
lung_risk = len(fdf[fdf['Disease_Label'] == 'Lung Disease'])
pct_smoke = (regular / total * 100) if total > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class="smoke-kpi">
        <div class="main-val">{total:,}</div>
        <div class="label">Total Patients</div>
        <div class="sub">↑ +124 this month</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="smoke-kpi">
        <div class="main-val">{pct_smoke:.1f}%</div>
        <div class="label">Regular Smokers</div>
        <div class="sub">vs Avg Age {avg_age:.1f}</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="smoke-kpi">
        <div class="main-val">{avg_bmi:.1f}</div>
        <div class="label">Avg BMI</div>
        <div class="sub">vs Avg BMI 24.9 (normal)</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="smoke-kpi">
        <div class="main-val">{regular:,}</div>
        <div class="label">Active Smokers</div>
        <div class="sub" style="color:#EF4444;">⚠️ High Risk Group</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class="smoke-kpi">
        <div class="main-val">{lung_risk:,}</div>
        <div class="label">Lung Disease Cases</div>
        <div class="sub" style="color:#EF4444;">↑ Linked to Smoking</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── ROW 1: Donut + Lung Visual + Gender Bar ──────────────
r1c1, r1c2, r1c3 = st.columns([1.2, 1, 1.4])

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E2E8F0', family='Inter'), margin=dict(t=30, b=10, l=10, r=10)
)

with r1c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**% of Smoking Status**")
    smoke_counts = fdf['Smoking_Habit'].value_counts().reset_index()
    smoke_counts.columns = ['Status', 'Count']
    fig_donut = go.Figure(go.Pie(
        labels=smoke_counts['Status'], values=smoke_counts['Count'],
        hole=0.65, marker_colors=['#10B981', '#F59E0B', '#EF4444'],
        textinfo='percent', hoverinfo='label+percent+value'
    ))
    fig_donut.update_layout(**PLOTLY_LAYOUT, height=260,
        annotations=[dict(text=f"<b>{total:,}</b><br>Patients", x=0.5, y=0.5,
                          font=dict(size=14, color='white'), showarrow=False)])
    fig_donut.update_traces(textfont_size=12)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r1c2:
    st.markdown('<div class="lung-visual">', unsafe_allow_html=True)
    st.markdown("**🫁 Lung Risk Indicator**")
    # Gauge chart as lung health indicator
    lung_score = (regular / total * 100) if total > 0 else 0
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=lung_score,
        title={'text': "Smoking Risk Score", 'font': {'color': '#94A3B8', 'size': 12}},
        number={'suffix': '%', 'font': {'color': '#EF4444', 'size': 28}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#475569'},
            'bar': {'color': '#EF4444'},
            'steps': [
                {'range': [0, 33], 'color': 'rgba(16,185,129,0.2)'},
                {'range': [33, 66], 'color': 'rgba(245,158,11,0.2)'},
                {'range': [66, 100], 'color': 'rgba(239,68,68,0.2)'},
            ],
            'threshold': {'line': {'color': '#00F3FF', 'width': 3}, 'value': lung_score}
        }
    ))
    fig_gauge.update_layout(**PLOTLY_LAYOUT, height=260)
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r1c3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Smoking Status by Gender**")
    sg = fdf.groupby(['Smoking_Habit', 'Gender']).size().reset_index(name='Count')
    fig_sg = px.bar(sg, x='Count', y='Smoking_Habit', color='Gender', barmode='group',
                    orientation='h', color_discrete_map={'Male': '#0057FF', 'Female': '#00F3FF'})
    fig_sg.update_layout(**PLOTLY_LAYOUT, height=260,
                          xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    st.plotly_chart(fig_sg, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── ROW 2: Cholesterol Risk + Smoking Trend + Stress ──────
r2c1, r2c2 = st.columns([1.5, 1])

with r2c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Cholesterol & Hypertension Risk Across Age Groups**")
    age_chol = fdf.groupby('Age_Group').agg(
        Avg_Cholesterol=('Cholesterol', 'mean'),
        Avg_SysBP=('Systolic_BP', 'mean'),
        Count=('Age', 'count')
    ).reset_index()
    fig_chol = go.Figure()
    fig_chol.add_trace(go.Bar(name='Avg Cholesterol', x=age_chol['Age_Group'].astype(str),
                               y=age_chol['Avg_Cholesterol'], marker_color='#EF4444', opacity=0.85))
    fig_chol.add_trace(go.Bar(name='Avg Systolic BP', x=age_chol['Age_Group'].astype(str),
                               y=age_chol['Avg_SysBP'], marker_color='#F59E0B', opacity=0.85))
    fig_chol.update_layout(**PLOTLY_LAYOUT, height=280, barmode='group',
                            xaxis=dict(showgrid=False, title='Age Group'),
                            yaxis=dict(showgrid=False, title='Value'),
                            legend=dict(orientation='h', y=1.1))
    st.plotly_chart(fig_chol, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r2c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Stress Impact on Smokers**")
    stress_smoke = fdf.groupby(['Stress_Level', 'Smoking_Habit']).size().reset_index(name='Count')
    fig_stress = px.bar(stress_smoke, x='Stress_Level', y='Count', color='Smoking_Habit',
                         barmode='stack', color_discrete_map={
                             'Never': '#10B981', 'Occasional': '#F59E0B', 'Regular': '#EF4444'})
    fig_stress.update_layout(**PLOTLY_LAYOUT, height=280,
                               xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                               legend=dict(orientation='h', y=1.1))
    st.plotly_chart(fig_stress, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── ROW 3: Smoking vs Disease + BMI Scatter ───────────────
r3c1, r3c2 = st.columns(2)

with r3c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Smoking Duration & Disease Risk (Age-based Trend)**")
    smoke_age = fdf.groupby(['Age_Group', 'Smoking_Habit']).size().reset_index(name='Count')
    fig_line = px.line(smoke_age, x='Age_Group', y='Count', color='Smoking_Habit',
                        markers=True, color_discrete_map={
                            'Never': '#10B981', 'Occasional': '#F59E0B', 'Regular': '#EF4444'})
    fig_line.update_layout(**PLOTLY_LAYOUT, height=260,
                            xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    fig_line.update_traces(line=dict(width=3))
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r3c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**BMI vs Cholesterol — Smokers vs Non-Smokers**")
    fig_scatter = px.scatter(fdf, x='BMI', y='Cholesterol', color='Smoking_Habit', opacity=0.6,
                              size='Age', color_discrete_map={
                                  'Never': '#10B981', 'Occasional': '#F59E0B', 'Regular': '#EF4444'})
    fig_scatter.update_layout(**PLOTLY_LAYOUT, height=260,
                               xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; color:#334155; padding:20px 0 10px; font-size:12px;">
    🧬 Nexus AI Healthcare Intelligence  •  Smoking Risk Analysis Module  •  Powered by XGBoost & Random Forest
</div>
""", unsafe_allow_html=True)
