import os
import requests
import json
from datetime import datetime

API_KEY = "wejdamed8baj4kpq"
ACCESS_TOKEN_FILE = "access_token.txt"
OUTPUT_FOLDER = "trade_data"

with open(ACCESS_TOKEN_FILE, "r") as f:
    ACCESS_TOKEN = f.read().strip()

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def fetch_positions():
    url = "https://api.kite.trade/portfolio/positions"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get("data", {})
        positions = data.get("day", [])
        open_positions = [pos for pos in positions if pos.get("quantity", 0) != 0]
        output_file = os.path.join(OUTPUT_FOLDER, "open_positions.json")
        with open(output_file, "w") as f:
            json.dump(open_positions, f, indent=4)
        print(f"{datetime.now()} - Saved {len(open_positions)} open positions to {output_file}")
        return open_positions
    else:
        print(f"{datetime.now()} - Error {response.status_code}: {response.text}")
        return []

if __name__ == "__main__":
    print(f"{datetime.now()} - Fetching open positions")
    positions = fetch_positions()
    print(f"{datetime.now()} - Completed fetching positions")
