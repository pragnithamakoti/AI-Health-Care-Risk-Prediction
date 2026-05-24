import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Dark Theme & Typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0B0E14; /* Deep dark background */
            color: #E2E8F0;
        }
        
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 24px;
            margin: 10px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0, 243, 255, 0.1);
            border-color: rgba(0, 243, 255, 0.2);
        }
        
        /* KPI Metrics */
        .kpi-title {
            font-size: 14px;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        
        .kpi-value {
            font-size: 36px;
            font-weight: 700;
            color: #FFFFFF;
            margin: 0;
            text-shadow: 0 0 20px rgba(0, 243, 255, 0.4);
        }
        
        .kpi-delta {
            font-size: 14px;
            font-weight: 600;
            margin-top: 8px;
        }
        .delta-up { color: #10B981; }
        .delta-down { color: #EF4444; }
        
        /* Neon Highlights */
        .neon-text {
            color: #00F3FF;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #0057FF 0%, #00F3FF 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            box-shadow: 0 0 20px rgba(0, 243, 255, 0.6);
            transform: translateY(-2px);
            color: white;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #121826 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_kpi_card(title, value, delta=None, delta_type="up"):
    delta_class = "delta-up" if delta_type == "up" else "delta-down"
    delta_html = f'<div class="kpi-delta {delta_class}">{delta}</div>' if delta else ""
    
    st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_alert(message, type="info"):
    colors = {
        "info": "#00F3FF",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "success": "#10B981"
    }
    color = colors.get(type, "#00F3FF")
    
    st.markdown(f"""
        <div style="
            border-left: 4px solid {color};
            background: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1);
            padding: 16px;
            border-radius: 4px;
            color: #E2E8F0;
            margin: 10px 0;
        ">
            {message}
        </div>
    """, unsafe_allow_html=True)
