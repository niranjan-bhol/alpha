import os
import json
from datetime import datetime

OPEN_POSITIONS_FILE = os.path.join("trade_data", "open_positions.json")
QUOTES_FILE = os.path.join("mkt_quotes", "quotes.json")
OUTPUT_DIR = "payloads"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "exit_payload.py")

def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def build_exit_payloads(positions, quotes):
    payloads = []
    quote_data = quotes.get("data", {})
    for pos in positions:
        qty = pos.get("quantity", 0)
        if qty == 0:
            continue
        nse_symbol = f"NSE:{pos['tradingsymbol']}"
        if nse_symbol not in quote_data:
            continue
        transaction_type = "BUY" if qty < 0 else "SELL"
        depth = quote_data[nse_symbol].get("depth", {})
        price = None
        if transaction_type == "BUY":
            sell_depth = depth.get("sell", [])
            if sell_depth:
                price = sell_depth[0]["price"]
        else:
            buy_depth = depth.get("buy", [])
            if buy_depth:
                price = buy_depth[0]["price"]
        if price is None:
            continue
        payloads.append({
            "tradingsymbol": pos["tradingsymbol"],
            "exchange": pos["exchange"],
            "transaction_type": transaction_type,
            "order_type": "LIMIT",
            "quantity": str(abs(qty)),
            "product": pos["product"],
            "price": price,
            "validity": "DAY",
            "tag": "eprs_2_ex"
        })
    return payloads

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    positions = load_json(OPEN_POSITIONS_FILE)
    quotes = load_json(QUOTES_FILE)
    exit_payloads = build_exit_payloads(positions, quotes)
    with open(OUTPUT_FILE, "w") as f:
        f.write("exit_payloads = ")
        json.dump(exit_payloads, f, indent=4)
    print(f"{datetime.now()} - Exit payloads exported to {OUTPUT_FILE}")
