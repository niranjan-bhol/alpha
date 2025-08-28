import requests
import json
import os
from datetime import datetime
from pre_data import nse_symbols

def load_access_token(file_path="access_token.txt"):
    with open(file_path) as f:
        return f.read().strip()

def fetch_open_prices(api_key, access_token, symbols):
    url = "https://api.kite.trade/quote/ohlc"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {api_key}:{access_token}"
    }
    params = {"i": symbols}
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get("data", {})
    return {symbol.split(":")[1]: info["ohlc"]["open"] for symbol, info in data.items()}

def save_to_file(data, folder, filename):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, filename)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    return file_path

if __name__ == "__main__":
    api_key = "wejdamed8baj4kpq"
    access_token = load_access_token()
    open_prices = fetch_open_prices(api_key, access_token, nse_symbols)
    file_path = save_to_file(open_prices, "todays_data", "open_prices.json")
    print(f"{datetime.now()} - Open prices saved to {file_path}")
