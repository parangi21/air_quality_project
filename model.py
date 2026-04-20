import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load data
data = pd.read_csv("air_quality.csv", encoding='latin1', low_memory=False)

# Select only useful columns (based on YOUR dataset)
data = data[['so2', 'no2', 'rspm', 'spm', 'pm2_5']]

# Convert to numeric (handle errors)
data = data.apply(pd.to_numeric, errors='coerce')

# Fill missing values instead of dropping everything
data = data.fillna(data.mean())

# Features & Target
X = data[['so2', 'no2', 'rspm', 'spm']]
y = data['pm2_5']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print(" Model trained & saved successfully!")