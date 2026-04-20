import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import numpy as np

# Firebase setup
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://air-project-14108-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

ref = db.reference("air_quality")

# Load dataset
data = pd.read_csv("air_quality.csv", encoding='latin1', low_memory=False)

# Select columns
data = data[['so2', 'no2', 'rspm', 'spm', 'pm2_5']]

# Clean data
data = data.replace(['NA', 'NaN', '--', ' ', 'None', 'nan'], np.nan)
data = data.apply(pd.to_numeric, errors='coerce')

# Fix invalid values
data = data.fillna(0)
data = data.replace([np.inf, -np.inf], 0)

# Limit rows (important)
data = data.head(500)

print("🚀 Rows to upload:", len(data))

count = 0

for i, row in data.iterrows():
    try:
        ref.push({
            "SO2": float(row['so2']),
            "NO2": float(row['no2']),
            "RSPM": float(row['rspm']),
            "SPM": float(row['spm']),
            "PM25": float(row['pm2_5'])   # 🔥 FIXED HERE
        })

        count += 1

        if count % 50 == 0:
            print(f"✅ Uploaded {count} rows")

    except Exception as e:
        print(f"❌ Error row {i}: {e}")

print("\n🎉 Upload complete!")
print("📊 Total uploaded:", count)