import os
import json
import requests
from datetime import datetime

API_KEY = "wejdamed8baj4kpq"
ACCESS_TOKEN_FILE = "access_token.txt"
OUTPUT_FOLDER = "todays_data"
OUTPUT_FILE = "margin.json"

def format_inr(number):
    s = f"{number:,.2f}"
    integer_part, decimal_part = s.split(".")
    integer_part = integer_part.replace(",", "")
    if len(integer_part) > 3:
        last3 = integer_part[-3:]
        rest = integer_part[:-3]
        groups = []
        while len(rest) > 2:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.insert(0, rest)
        formatted_int = ",".join(groups + [last3])
    else:
        formatted_int = integer_part
    return f"₹{formatted_int}.{decimal_part}"

def get_equity_margin(api_key, access_token):
    url = "https://api.kite.trade/user/margins"
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {api_key}:{access_token}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]["equity"]["net"]

def calc_margins(api_key, access_token):
    equity_net = get_equity_margin(api_key, access_token)
    leverage_margin = equity_net * 5
    discounted_margin = leverage_margin * 0.95
    return {
        "available_margin": equity_net,
        "leveraged_margin": leverage_margin,
        "discounted_margin": discounted_margin,
    }

def format_margins(margin_dict):
    return {key: format_inr(value) for key, value in margin_dict.items()}

def save_margins(margins, folder=OUTPUT_FOLDER, filename=OUTPUT_FILE):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, "w") as f:
        json.dump(margins, f, indent=4)
    print(f"{datetime.now()} - Saved margin data to {filepath}")

if __name__ == "__main__":
    with open(ACCESS_TOKEN_FILE, "r") as f:
        ACCESS_TOKEN = f.read().strip()
    margins = calc_margins(API_KEY, ACCESS_TOKEN)
    formatted = format_margins(margins)
    print(f"Available Margin  : {formatted['available_margin']}")
    print(f"Leveraged Margin  : {formatted['leveraged_margin']}")
    print(f"Discounted Margin : {formatted['discounted_margin']}")
    save_margins(margins)
