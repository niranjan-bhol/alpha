import os
import json
from datetime import datetime
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from pre_data import PAIRS

HISTORICAL_FOLDER = "historical_data"
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

def train_model(etf_df, underlying_df):
    merged = pd.merge(
        etf_df[["datetime", "close"]],
        underlying_df[["datetime", "close"]],
        on="datetime", suffixes=("_etf", "_underlying")
    )
    X = merged["close_underlying"].to_numpy().reshape(-1, 1)
    y = merged["close_etf"].to_numpy()
    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)
    return model

def predict_open(model, underlying_open_price):
    return float(model.predict(np.array([[underlying_open_price]]))[0])

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
        model = train_model(etf_df, underlying_df)
        predictions[etf] = predict_open(model, todays_open[underlying])
    output_file = save_predictions(predictions)
    print(f"{datetime.now()} - Saved all predicted open prices to {output_file}")
