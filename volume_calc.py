import pandas as pd
import os
import json
from datetime import datetime
from pre_data import etf_files

def calculate_safe_volumes(historical_folder, etf_files):
    predicted_volumes = {}
    for etf_file in etf_files:
        etf_name = etf_file.replace(".csv", "")
        df = pd.read_csv(os.path.join(historical_folder, etf_file))
        last_60_volumes = df.iloc[-60:, 2]
        avg_volume = last_60_volumes.mean() / 5000
        predicted_volumes[etf_name] = avg_volume
    return predicted_volumes

def save_volumes(predicted_volumes, output_file):
    with open(output_file, "w") as f:
        json.dump(predicted_volumes, f, indent=4)
    print(f"{datetime.now()} - redicted volumes saved to {output_file}")

if __name__ == "__main__":
    historical_folder = "historical_data"
    predicted_folder = "predicted_data"
    os.makedirs(predicted_folder, exist_ok=True)
    output_file = os.path.join(predicted_folder, "safe_volumes.json")
    predicted_volumes = calculate_safe_volumes(historical_folder, etf_files)
    save_volumes(predicted_volumes, output_file)
