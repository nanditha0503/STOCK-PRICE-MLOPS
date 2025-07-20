import pandas as pd
import yaml
from sklearn.linear_model import LinearRegression
import pickle
import os
import mlflow
import mlflow.sklearn
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

# ✅ Load parameters
with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

ticker = params["data"]["ticker"]
start_date = params["data"]["start_date"]
end_date = params["data"]["end_date"]
test_size = params["train"]["test_size"]
random_state = params["train"]["random_state"]

# ✅ Load and clean data
df = pd.read_csv("data/raw_data.csv")
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df.dropna(subset=["Date", "Close"], inplace=True)
df["DateOrdinal"] = df["Date"].apply(lambda x: x.toordinal())

# ✅ Train model
X = df[["DateOrdinal"]]
y = df["Close"]
model = LinearRegression()
model.fit(X, y)

# ✅ MLflow tracking
with mlflow.start_run():
    mlflow.log_param("ticker", ticker)
    mlflow.log_param("start_date", start_date)
    mlflow.log_param("end_date", end_date)
    mlflow.log_param("random_state", random_state)
    mlflow.log_param("test_size", test_size)
    
    # Metrics
    y_pred = model.predict(X)
    r2 = model.score(X, y)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    
    mlflow.log_metric("r2_score", r2)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mae", mae)

    # Save model with unique name
    run_id = mlflow.active_run().info.run_id
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"models/model_{timestamp}.pkl"
    os.makedirs("models", exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    # Log model and artifact
    mlflow.log_artifact(model_path)
    mlflow.sklearn.log_model(sk_model=model, artifact_path="model", registered_model_name="StockPriceModel")

    # Tags
    mlflow.set_tag("experiment", "stock_price")
    mlflow.set_tag("model_type", "LinearRegression")

print("✅ Model trained, saved, and tracked with MLflow.")
