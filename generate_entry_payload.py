import os
import json
from datetime import datetime

ADJUSTED_VOLUMES_FILE = os.path.join("predicted_data", "adjusted_volumes.json")
PRICES_FILE = os.path.join("predicted_data", "payload_prices.json")
OUTPUT_DIR = "payloads"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry_payload.py")

def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def build_payloads(volumes, prices):
    payloads = []
    for etf, quantity in volumes.items():
        buy_price = prices[etf]["buy_price"]
        sell_price = prices[etf]["sell_price"]
        payloads.append({
            "tradingsymbol": etf,
            "exchange": "NSE",
            "transaction_type": "BUY",
            "order_type": "LIMIT",
            "quantity": str(quantity),
            "price": buy_price,
            "product": "MIS",
            "validity": "DAY",
            "tag": "eprs_1_en"
        })
        payloads.append({
            "tradingsymbol": etf,
            "exchange": "NSE",
            "transaction_type": "SELL",
            "order_type": "LIMIT",
            "quantity": str(quantity),
            "price": sell_price,
            "product": "MIS",
            "validity": "DAY",
            "tag": "eprs_1_en"
        })
    return payloads

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    volumes = load_json(ADJUSTED_VOLUMES_FILE)
    prices = load_json(PRICES_FILE)
    payloads = build_payloads(volumes, prices)
    with open(OUTPUT_FILE, "w") as f:
        f.write("entry_payloads = ")
        json.dump(payloads, f, indent=4)
    print(f"{datetime.now()} - Payloads exported to {OUTPUT_FILE}")
