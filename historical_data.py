import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from pre_data import UNDERLYING_TOKENS, ETF_TOKENS

API_KEY = "wejdamed8baj4kpq"
ACCESS_TOKEN_FILE = "access_token.txt"
INTERVAL = "minute"
START_DATE = "2021-01-01"
OUTPUT_FOLDER = "historical_data"

with open(ACCESS_TOKEN_FILE, "r") as f:
    ACCESS_TOKEN = f.read().strip()

start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
end_date = datetime.today() - timedelta(days=1)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def fetch_candles(symbol, token):
    url = f"https://api.kite.trade/instruments/historical/{token}/{INTERVAL}"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}",
    }

    all_candles = []
    chunk_start = start_date
    while chunk_start < end_date:
        chunk_end = min(chunk_start + timedelta(days=60), end_date)
        params = {
            "from": chunk_start.strftime("%Y-%m-%d %H:%M:%S"),
            "to": chunk_end.strftime("%Y-%m-%d %H:%M:%S")
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json().get("data", {})
        candles = data.get("candles", [])
        all_candles.extend(candles)
        chunk_start = chunk_end + timedelta(days=1)

    if not all_candles:
        print(f"{datetime.now()} - No data for {symbol}")
        return None

    df = pd.DataFrame(all_candles, columns=["datetime", "open", "high", "low", "close", "volume"])
    df = df[["datetime", "close", "volume"]]
    output_file = os.path.join(OUTPUT_FOLDER, f"{symbol}.csv")
    df.to_csv(output_file, index=False)
    print(f"{datetime.now()} - Saved {len(df)} rows for {symbol} to {output_file}")
    return df

def fetch_all(symbol_dict):
    all_data = {}
    for symbol, token in symbol_dict.items():
        df = fetch_candles(symbol, token)
        if df is not None:
            all_data[symbol] = df
    return all_data

if __name__ == "__main__":
    print(f"{datetime.now()} - Fetching underlying assets")
    underlying_data = fetch_all(UNDERLYING_TOKENS)
    print(f"{datetime.now()} - Fetching ETF symbols")
    etf_data = fetch_all(ETF_TOKENS)
    print(f"{datetime.now()} - Completed fetching all candles.")
