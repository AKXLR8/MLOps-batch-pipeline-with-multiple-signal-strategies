import numpy as np


def generate_signals(df, config):
    window = config["window"]
    signal_type = config.get("signal_type", "basic")
    threshold = config.get("z_threshold", 0.5)

    # Rolling statistics
    df["rolling_mean"] = df["close"].rolling(window).mean()
    df["rolling_std"] = df["close"].rolling(window).std()

    # Handle zero std (avoid division by zero)
    df["rolling_std"] = df["rolling_std"].replace(0, np.nan)

    # Explicit NaN handling (assignment requirement)
    df = df.dropna(subset=["rolling_mean", "rolling_std"])

    # --- BASIC SIGNAL ---
    df["basic_signal"] = (df["close"] > df["rolling_mean"]).astype(int)

    # --- Z-SCORE SIGNAL ---
    df["z_score"] = (df["close"] - df["rolling_mean"]) / df["rolling_std"]
    df["z_signal"] = (df["z_score"] > threshold).astype(int)

    # --- FINAL SIGNAL SELECTION ---
    if signal_type == "basic":
        df["signal"] = df["basic_signal"]

    elif signal_type == "zscore":
        df["signal"] = df["z_signal"]

    elif signal_type == "hybrid":
        # Strong confirmation signal
        df["signal"] = ((df["basic_signal"] == 1) & (df["z_signal"] == 1)).astype(int)

    else:
        raise ValueError(f"Invalid signal_type: {signal_type}")

    return df