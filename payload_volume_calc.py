import os
import json
from datetime import datetime

MARGIN_FILE = os.path.join("todays_data", "margin.json")
SAFE_VOLUMES_FILE = os.path.join("predicted_data", "safe_volumes.json")
PRICES_FILE = os.path.join("predicted_data", "payload_prices.json")
OUTPUT_FILE = os.path.join("predicted_data", "adjusted_volumes.json")

def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def calculate_adjusted_volumes(safe_volumes, prices, discounted_margin):
    total_required = sum(volume * prices[etf]["sell_price"] for etf, volume in safe_volumes.items())
    adjusted = {}
    for etf, volume in safe_volumes.items():
        calc_vol = (volume * discounted_margin) / total_required
        adjusted[etf] = min(int(round(calc_vol)), int(volume))
    return adjusted

if __name__ == "__main__":
    margin_data = load_json(MARGIN_FILE)
    safe_volumes = load_json(SAFE_VOLUMES_FILE)
    buy_sell_prices = load_json(PRICES_FILE)
    adjusted_volumes = calculate_adjusted_volumes(safe_volumes, buy_sell_prices, margin_data["discounted_margin"])
    save_json(adjusted_volumes, OUTPUT_FILE)
    print(f"{datetime.now()} - Adjusted volumes saved to {OUTPUT_FILE}")
