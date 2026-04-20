import streamlit as st
import json
from firebase_admin import credentials, db
import firebase_admin

# Convert secrets to proper dict
firebase_dict = dict(st.secrets["firebase_key"])

# Fix private key formatting
firebase_dict["private_key"] = firebase_dict["private_key"].replace("\\n", "\n")

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://air-project-14108-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })