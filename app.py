import streamlit as st
import time
from utils.auth import login_user, logout_user, create_default_accounts
from utils.ui_components import apply_custom_css, render_alert

# Page Config must be the first Streamlit command
st.set_page_config(
    page_title="Nexus Healthcare Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply premium dark theme CSS
apply_custom_css()

# Initialize Database and default accounts
create_default_accounts()

def login_page():
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🧬 <span class='neon-text'>Nexus</span> Healthcare AI</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>System Access</h3>", unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Authenticate"):
            with st.spinner("Verifying credentials..."):
                time.sleep(1) # Simulation for premium feel
                if login_user(username, password):
                    st.success("Authentication successful! Redirecting...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    render_alert("Invalid credentials. Please try again.", "danger")
                    
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='margin-top: 2rem; text-align: center; color: #64748B; font-size: 0.9rem;'>
            <p>Default Access Credentials:</p>
            <code>Admin: admin/admin123</code><br>
            <code>Doctor: doctor/doctor123</code><br>
            <code>Analyst: analyst/analyst123</code>
        </div>
        """, unsafe_allow_html=True)

def main_app():
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'><span class='neon-text'>Nexus</span> AI</h2>", unsafe_allow_html=True)
        st.markdown(f"**User:** {st.session_state['username']}")
        st.markdown(f"**Role:** {st.session_state['role']}")
        st.divider()
        
        st.markdown("### Navigation")
        st.markdown("👈 Select a module from the pages menu above.")
        
        st.divider()
        if st.button("Logout", key="logout_btn"):
            logout_user()
            st.rerun()
            
    # Welcome Screen
    st.markdown(f"<h1>Welcome back, <span class='neon-text'>{st.session_state['username'].capitalize()}</span></h1>", unsafe_allow_html=True)
    st.markdown("### System Status: <span style='color:#10B981;'>Online</span>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3>🚀 Quick Start Guide</h3>
        <p>Select a module from the sidebar to begin:</p>
        <ul>
            <li><strong>Dashboard:</strong> Executive overview and high-level KPIs.</li>
            <li><strong>AI Prediction:</strong> Run patient vitals through our ML models.</li>
            <li><strong>Patient Analytics:</strong> In-depth demographic and risk analysis.</li>
            <li><strong>Admin Panel:</strong> Manage system users and audit logs.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_page()
else:
    main_app()
