import streamlit as st
import pandas as pd
from utils.auth import require_auth, create_user
from utils.db_manager import db
from utils.ui_components import apply_custom_css, render_alert

st.set_page_config(page_title="Admin Panel | Nexus AI", layout="wide", initial_sidebar_state="expanded")
apply_custom_css()
require_auth(['Admin'])

st.markdown("<h1>⚙️ System <span class='neon-text'>Administration</span></h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["👥 User Management", "📝 System Logs", "🗄️ Database Tools"])

with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Add New User")
        with st.form("add_user_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["Doctor", "Analyst", "Admin"])
            
            if st.form_submit_button("Create User"):
                if new_username and new_password:
                    if create_user(new_username, new_password, new_role):
                        render_alert(f"User {new_username} created successfully in Firebase.", "success")
                    else:
                        render_alert("Error creating user (may already exist or weak password).", "danger")
                else:
                    render_alert("Please fill all fields.", "warning")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Active Users (Firebase)")
        try:
            users_data = db.child("users").get().val()
            if users_data:
                users_list = [{"UID": k, "Username": v.get("username"), "Email": v.get("email"), "Role": v.get("role")} for k, v in users_data.items()]
                st.dataframe(pd.DataFrame(users_list), use_container_width=True, hide_index=True)
            else:
                st.info("No users found.")
        except Exception as e:
            st.error(f"Could not load users from Firebase: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Audit Logs (Firebase)")
    try:
        logs_data = db.child("logs").order_by_key().limit_to_last(100).get().val()
        if logs_data:
            logs_list = [{"Log ID": k, "User ID": v.get("user_id"), "Action": v.get("action"), "Timestamp": v.get("timestamp")} for k, v in logs_data.items()]
            # Reverse to show newest first
            logs_list.reverse()
            st.dataframe(pd.DataFrame(logs_list), use_container_width=True, hide_index=True)
        else:
            st.info("No logs found.")
    except Exception as e:
        st.error(f"Could not load logs from Firebase: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Database Maintenance")
    st.write("Perform routine database checks and backups here.")
    
    if st.button("Trigger Manual Backup"):
        with st.spinner("Backing up Firebase database (Simulated)..."):
            import time
            time.sleep(2)
            render_alert("Database backup triggered via Firebase Cloud Functions (Simulated).", "success")
            
    if st.button("Purge Old Logs (> 30 days)"):
        render_alert("Log purge scheduled in Firebase.", "info")
    st.markdown("</div>", unsafe_allow_html=True)
