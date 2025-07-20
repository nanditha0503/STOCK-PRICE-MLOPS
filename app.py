# app.py
from fastapi import FastAPI
import pandas as pd
import pickle
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

instrumentator = Instrumentator().instrument(app).expose(app)

model = pickle.load(open("models/model.pkl", "rb"))

@app.get("/")
def read_root():
    return {"message": "Stock Price Predictor is Live"}

@app.get("/predict")
def predict(date: str):
    try:
        date_ordinal = pd.to_datetime(date).toordinal()
        pred = model.predict([[date_ordinal]])[0]
        return {"predicted_close": round(pred, 2)}
    except Exception as e:
        return {"error": str(e)}
