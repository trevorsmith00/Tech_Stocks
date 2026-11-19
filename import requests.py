import os
import requests
import pandas as pd

# Read the API key from an environment variable so it is never committed to the repo.
# Set it before running:  export ALPHAVANTAGE_API_KEY="your_key"   (Windows: setx ALPHAVANTAGE_API_KEY "your_key")
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
if not api_key:
    raise SystemExit("Missing ALPHAVANTAGE_API_KEY environment variable. Get a free key at https://www.alphavantage.co/support/#api-key")
symbols = ["AAPL", "MSFT", "GOOGL", "NVDA", "PLTR", "META", "CRM"]
all_data = []

for symbol in symbols:
    print(f"Fetching {symbol}...")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df["Symbol"] = symbol
    df["Date"] = df.index
    all_data.append(df.reset_index(drop=True))

# Combine all data
combined_df = pd.concat(all_data)
combined_df.to_csv("stocks_combined.csv", index=False)
print("✅ CSV saved: stocks_combined.csv")
