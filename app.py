import streamlit as st
import pandas as pd
import pickle
import firebase_admin
from firebase_admin import credentials, db

# -----------------------------
# Load ML Model
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))

# -----------------------------
# Firebase Setup (CORRECT ✅)
# -----------------------------
if not firebase_admin._apps:
    firebase_dict = st.secrets["firebase_key"]  # from Streamlit secrets
    cred = credentials.Certificate(firebase_dict)

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://air-project-14108-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# -----------------------------
# Fetch Data from Firebase
# -----------------------------
ref = db.reference("air_quality")
data = ref.get()

if data:
    df = pd.DataFrame(data.values())
else:
    df = pd.DataFrame()

# -----------------------------
# UI
# -----------------------------
st.title("🌍 Cloud-Based Air Quality Monitoring System")

if not df.empty:
    st.subheader("📊 Air Quality Data")
    st.dataframe(df)

    st.subheader("📈 Pollution Trends")

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_cols) > 0:
        st.line_chart(df[numeric_cols])
    else:
        st.warning("No numeric data available for graph")

else:
    st.warning("⚠ No data found in Firebase")

# -----------------------------
# Prediction Section
# -----------------------------
st.subheader("🔮 Predict PM2.5 Level")

so2 = st.number_input("SO2", min_value=0.0)
no2 = st.number_input("NO2", min_value=0.0)
rspm = st.number_input("RSPM", min_value=0.0)
spm = st.number_input("SPM", min_value=0.0)

if st.button("Predict"):
    try:
        result = model.predict([[so2, no2, rspm, spm]])
        st.success(f"✅ Predicted PM2.5: {result[0]:.2f}")
    except Exception as e:
        st.error(f"Error in prediction: {e}")