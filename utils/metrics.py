import time
def compute_metrics(df, config, start_time):
    latency = int((time.time() - start_time) * 1000)

    signal_rate = df["signal"].mean()

    return {
        "version": config["version"],
        "rows_processed": len(df),
        "metric": "signal_rate",
        "value": round(float(signal_rate), 4),
        "latency_ms": latency,
        "seed": config["seed"],
        "status": "success"
    }