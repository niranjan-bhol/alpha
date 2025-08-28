import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from pre_data import UNDERLYING_TOKENS, ETF_TOKENS

API_KEY = "wejdamed8baj4kpq"
ACCESS_TOKEN_FILE = "access_token.txt"
INTERVAL = "day"
START_DATE = "2021-01-01"
OUTPUT_FOLDER = "historical_data"

with open(ACCESS_TOKEN_FILE, "r") as f:
    ACCESS_TOKEN = f.read().strip()

start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
end_date = datetime.today() - timedelta(days=1)
FROM_TIME = start_date.strftime("%Y-%m-%d 09:15:00")
TO_TIME = end_date.strftime("%Y-%m-%d 16:00:00")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def fetch_candles(symbol, token):
    url = f"https://api.kite.trade/instruments/historical/{token}/{INTERVAL}"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}",
    }
    params = {"from": FROM_TIME, "to": TO_TIME}
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get("data", {})
    candles = data.get("candles", [])
    df = pd.DataFrame(candles, columns=["datetime", "open", "high", "low", "close", "volume"])
    df = df[["datetime", "close", "volume"]]
    output_file = os.path.join(OUTPUT_FOLDER, f"{symbol}.csv")
    df.to_csv(output_file, index=False)
    print(f"{datetime.now()} - Saved {len(df)} rows for {symbol} to {output_file}")
    return df

def fetch_all(symbol_dict):
    all_data = {}
    for symbol, token in symbol_dict.items():
        all_data[symbol] = fetch_candles(symbol, token)
    return all_data

if __name__ == "__main__":
    print(f"{datetime.now()} - Fetching underlying assets")
    underlying_data = fetch_all(UNDERLYING_TOKENS)
    print(f"{datetime.now()} - Fetching ETF symbols")
    etf_data = fetch_all(ETF_TOKENS)
    print(f"{datetime.now()} - Completed fetching all candles.")
