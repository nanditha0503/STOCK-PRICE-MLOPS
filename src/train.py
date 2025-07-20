import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

# Load cleaned data
df = pd.read_csv("data/raw_data.csv")

# Parse date column and handle invalid values
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df.dropna(subset=["Date"], inplace=True)

# Convert dates to ordinal format for regression
df["DateOrdinal"] = df["Date"].apply(lambda x: x.toordinal())

# Train a simple linear regression model
X = df[["DateOrdinal"]]
y = df["Close"]
model = LinearRegression()
model.fit(X, y)

# Ensure model directory exists
os.makedirs("models", exist_ok=True)

# Save model
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to models/model.pkl")
