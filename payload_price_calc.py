import os
import json
from datetime import datetime

INPUT_FILE = os.path.join("predicted_data", "predicted_prices.json")
OUTPUT_FILE = os.path.join("predicted_data", "payload_prices.json")

def load_predicted_prices(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def calculate_buy_sell(prices, factor=0.005):
    result = {}
    for etf, price in prices.items():
        result[etf] = {
            "buy_price": round(price * (1 - factor), 2),
            "sell_price": round(price * (1 + factor), 2)
        }
    return result

def save_prices(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    predicted_prices = load_predicted_prices(INPUT_FILE)
    buy_sell_prices = calculate_buy_sell(predicted_prices)
    save_prices(buy_sell_prices, OUTPUT_FILE)
    print(f"{datetime.now()} - Payload buy & sell prices saved to {OUTPUT_FILE}")
