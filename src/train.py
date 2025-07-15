import pandas as pd
import pickle
import yaml
import mlflow
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

params = yaml.safe_load(open("params.yaml"))

df = pd.read_csv("data/raw_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Date_ordinal"] = df["Date"].map(pd.Timestamp.toordinal)

X = df[["Date_ordinal"]]
y = df["Close"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=params["train"]["test_size"], random_state=params["train"]["random_state"])

model = LinearRegression()
mlflow.start_run()
mlflow.log_param("model_type", "LinearRegression")
model.fit(X_train, y_train)
mlflow.sklearn.log_model(model, "model")

with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)
