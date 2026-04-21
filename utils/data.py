import pandas as pd
import yaml
import numpy as np
import os


def load_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)

    required = ["seed", "window", "version"]
    for r in required:
        if r not in config:
            raise ValueError(f"Missing config field: {r}")

    np.random.seed(config["seed"])
    return config


def load_and_clean_data(path):
    # ✅ File existence check
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")

    df = pd.read_csv(path)

    # Fix malformed CSV
    if len(df.columns) == 1:
        df = df.iloc[:, 0].str.split(",", expand=True)

    # ✅ Validate structure BEFORE renaming
    if df.shape[1] < 5:
        raise ValueError("Invalid dataset: expected OHLCV format with 'close' column")

    # Assign columns
    df.columns = [
        "timestamp", "open", "high", "low",
        "close", "volume_btc", "volume_usd"
    ]

    # Convert numeric columns
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Drop rows where close is invalid
    df = df.dropna(subset=["close"])

    # Final validation
    if df.empty:
        raise ValueError("Dataset is empty after cleaning")

    if df["close"].isnull().all():
        raise ValueError("'close' column has no valid values")

    return df