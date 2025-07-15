import pandas as pd
import pickle
import yaml
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

params = yaml.safe_load(open("params.yaml"))

df = pd.read_csv("data/raw_data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Date_ordinal"] = df["Date"].map(pd.Timestamp.toordinal)

X = df[["Date_ordinal"]]
y = df["Close"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=params["train"]["test_size"], random_state=params["train"]["random_state"])

with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
print("MSE:", mse)
