import pyrebase
import streamlit as st
import datetime

# User's Firebase Configuration
firebaseConfig = {
    "apiKey": "AIzaSyCDpZIOATCCRAKl9Gcf79rL78kauvEw09o",
    "authDomain": "ai-health-care-risk-prediction.firebaseapp.com",
    "databaseURL": "https://ai-health-care-risk-prediction-default-rtdb.firebaseio.com",
    "projectId": "ai-health-care-risk-prediction",
    "storageBucket": "ai-health-care-risk-prediction.firebasestorage.app",
    "messagingSenderId": "422870056978",
    "appId": "1:422870056978:web:98a3b6a896a61fdbae18cb",
    "measurementId": "G-YPL6JRGGX8"
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)

# Get reference to Auth and Database
auth = firebase.auth()
db = firebase.database()

def log_action(user_id, action):
    try:
        log_data = {
            "user_id": user_id,
            "action": action,
            "timestamp": str(datetime.datetime.now())
        }
        db.child("logs").push(log_data)
    except Exception as e:
        print(f"Failed to log action: {e}")

# Note: We no longer need init_db() as Firebase creates tables on the fly, 
# but we can leave a stub so we don't break app.py imports if they exist.
def init_db():
    pass
