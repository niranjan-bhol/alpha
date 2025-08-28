import os
import json
import requests
from pre_data import symbols1
from datetime import datetime

api_key = "wejdamed8baj4kpq"
with open("access_token.txt", "r") as f:
    access_token = f.read().strip()

OPEN_POSITIONS_FILE = os.path.join("trade_data", "open_positions.json")
OUTPUT_DIR = "mkt_quotes"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "quotes.json")

def load_open_positions():
    with open(OPEN_POSITIONS_FILE, "r") as f:
        return json.load(f)

def get_matching_symbols(open_positions, watchlist):
    return [
        pos["tradingsymbol"]
        for pos in open_positions
        if pos["tradingsymbol"] in watchlist
    ]

def fetch_quotes(symbols):
    url = "https://api.kite.trade/quote"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {api_key}:{access_token}"
    }
    instruments = [f"NSE:{sym}" for sym in symbols]
    params = [("i", i) for i in instruments]
    response = requests.get(url, headers=headers, params=params)
    return response.json()

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    open_positions = load_open_positions()
    symbols_to_fetch = get_matching_symbols(open_positions, symbols1)
    data = fetch_quotes(symbols_to_fetch)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"{datetime.now()} - Quotes saved to {OUTPUT_FILE}")
