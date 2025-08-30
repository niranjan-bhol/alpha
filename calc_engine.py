import os
import json
from datetime import datetime
import pandas as pd
from pre_data import PAIRS

HISTORICAL_FOLDER = "historical_data_price"
TODAYS_FOLDER = "todays_data"
PREDICTED_FOLDER = "predicted_data"

def load_historical(etf_file, underlying_file):
    etf_path = os.path.join(HISTORICAL_FOLDER, etf_file)
    underlying_path = os.path.join(HISTORICAL_FOLDER, underlying_file)
    etf_df = pd.read_csv(etf_path, parse_dates=["datetime"])
    underlying_df = pd.read_csv(underlying_path, parse_dates=["datetime"])
    return etf_df, underlying_df

def load_todays_open():
    path = os.path.join(TODAYS_FOLDER, "open_prices.json")
    with open(path) as f:
        return json.load(f)

def predict_open_ratio(etf_df, underlying_df, underlying_open_price, window=90):
    merged = pd.merge(
        etf_df[["datetime", "close"]],
        underlying_df[["datetime", "close"]],
        on="datetime",
        suffixes=("_etf", "_underlying")
    )
    merged["ratio"] = merged["close_etf"] / merged["close_underlying"]
    rolling_ratio = merged["ratio"].tail(window).mean()
    return float(underlying_open_price * rolling_ratio)

def save_predictions(predictions, filename="predicted_prices.json"):
    os.makedirs(PREDICTED_FOLDER, exist_ok=True)
    path = os.path.join(PREDICTED_FOLDER, filename)
    with open(path, "w") as f:
        json.dump(predictions, f, indent=4)
    return path

if __name__ == "__main__":
    todays_open = load_todays_open()
    predictions = {}
    for etf, underlying in PAIRS.items():
        etf_df, underlying_df = load_historical(f"{etf}.csv", f"{underlying}.csv")
        predictions[etf] = predict_open_ratio(
            etf_df, underlying_df, todays_open[underlying], window=90
        )
    output_file = save_predictions(predictions)
    print(f"{datetime.now()} - Saved all predicted open prices to {output_file}")
