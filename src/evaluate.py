import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

# Load test data
df = pd.read_csv("data/raw_data.csv")

# Ensure Date column is datetime and handle NaT
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df.dropna(subset=["Date"], inplace=True)
df["DateOrdinal"] = df["Date"].apply(lambda x: x.toordinal())

# Make predictions
X_test = df[["DateOrdinal"]]
y_test = df["Close"]
y_pred = model.predict(X_test)

# Evaluate
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"✅ Evaluation Complete:\n   RMSE: {rmse:.2f}\n   R² Score: {r2:.4f}")
import json

metrics = {
    "rmse": round(mean_squared_error(y_test, y_pred) ** 0.5, 2),
    "r2": round(r2_score(y_test, y_pred), 4)
}


with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("✅ Evaluation metrics saved to metrics.json")
