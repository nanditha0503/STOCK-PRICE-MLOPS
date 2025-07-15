import yfinance as yf
import pandas as pd
import os

# Parameters
ticker = "AAPL"
start = "2020-01-01"
end = "2023-01-01"

# Download stock data
df = yf.download(ticker, start=start, end=end)

# Reset index to move Date from index to column
df.reset_index(inplace=True)

# Optional: reduce columns if needed
# df = df[['Date', 'Close']]

# Ensure directory exists
os.makedirs("data", exist_ok=True)

# Save to CSV
df.to_csv("data/raw_data.csv", index=False)

print("✅ Saved cleaned data to data/raw_data.csv")

