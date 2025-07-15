import yfinance as yf
import pandas as pd
import yaml

params = yaml.safe_load(open("params.yaml"))["data"]
ticker, start, end = params["ticker"], params["start_date"], params["end_date"]

df = yf.download(ticker, start=start, end=end)
df.to_csv("data/raw_data.csv")
