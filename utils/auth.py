import streamlit as st
from utils.db_manager import auth, log_action

def get_email(username):
    """Convert username to Firebase-compatible email."""
    if "@" not in username:
        return f"{username.lower()}@nexus.ai"
    return username

def create_user(username, password, role):
    """Create a new user in Firebase Auth. Role is stored in session only."""
    email = get_email(username)
    try:
        user = auth.create_user_with_email_and_password(email, password)
        uid = user['localId']
        # Try to save role to DB - ignore if DB not set up
        try:
            from utils.db_manager import db
            db.child("users").child(uid).set({
                "username": username,
                "email": email,
                "role": role
            })
        except Exception:
            pass
        return True
    except Exception as e:
        err = str(e)
        if "EMAIL_EXISTS" in err:
            return False  # already exists
        print(f"Error creating user: {e}")
        return False

# Role mapping for default accounts (fallback if DB is not set up)
DEFAULT_ROLES = {
    "admin@nexus.ai": "Admin",
    "doctor@nexus.ai": "Doctor",
    "analyst@nexus.ai": "Analyst",
}

def login_user(username, password):
    """Sign in user via Firebase Auth."""
    email = get_email(username)
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        uid = user['localId']

        # Try to get role from Realtime Database first
        role = None
        actual_username = username
        try:
            from utils.db_manager import db
            user_data = db.child("users").child(uid).get().val()
            if user_data and 'role' in user_data:
                role = user_data['role']
                actual_username = user_data.get('username', username)
        except Exception:
            pass

        # Fallback to hardcoded role map if DB not available
        if role is None:
            role = DEFAULT_ROLES.get(email, "Doctor")

        st.session_state['user_id'] = uid
        st.session_state['username'] = actual_username
        st.session_state['role'] = role
        st.session_state['logged_in'] = True

        try:
            log_action(uid, "Logged in successfully")
        except Exception:
            pass

        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def logout_user():
    """Clear session state."""
    if 'user_id' in st.session_state:
        try:
            log_action(st.session_state['user_id'], "Logged out")
        except Exception:
            pass
    for key in ['user_id', 'username', 'role', 'logged_in']:
        if key in st.session_state:
            del st.session_state[key]

def create_default_accounts():
    """Create admin, doctor and analyst accounts in Firebase Auth."""
    accounts = [
        ("admin", "admin123", "Admin"),
        ("doctor", "doctor123", "Doctor"),
        ("analyst", "analyst123", "Analyst"),
    ]
    for username, password, role in accounts:
        create_user(username, password, role)

def require_auth(roles=None):
    """Stop page if user is not logged in or lacks the required role."""
    if not st.session_state.get('logged_in', False):
        st.warning("Please log in to access this page.")
        st.stop()
    if roles and st.session_state.get('role') not in roles:
        st.error(f"Access denied. Required role(s): {', '.join(roles)}")
        st.stop()
