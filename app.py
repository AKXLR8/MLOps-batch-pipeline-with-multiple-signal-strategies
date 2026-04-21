import streamlit as st
import pandas as pd
import numpy as np
import time

from utils.data import load_and_clean_data
from utils.signals import generate_signals
from utils.metrics import compute_metrics

st.set_page_config(page_title="MLOps Signal Dashboard", layout="wide")

st.title("MLOps Signal Pipeline Dashboard")

# Sidebar controls
st.sidebar.header(" Configuration")

signal_type = st.sidebar.selectbox(
    "Signal Type",
    ["basic", "zscore", "hybrid"]
)

window = st.sidebar.slider("Rolling Window", 2, 50, 5)
z_threshold = st.sidebar.slider("Z-score Threshold", 0.1, 2.0, 0.5)

# File upload
uploaded_file = st.file_uploader("Upload CSV (OHLCV format)", type=["csv"])

if uploaded_file is not None:
    try:
        # Save temp file
        df = pd.read_csv(uploaded_file)

        # Handle malformed CSV
        if len(df.columns) == 1:
            df = df.iloc[:, 0].str.split(",", expand=True)

        df.columns = [
            "timestamp", "open", "high", "low",
            "close", "volume_btc", "volume_usd"
        ]

        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["close"])

        config = {
            "window": window,
            "signal_type": signal_type,
            "z_threshold": z_threshold,
            "version": "ui",
            "seed": 42
        }

        start_time = time.time()

        df = generate_signals(df, config)

        metrics = compute_metrics(df, config, start_time)

        # Display metrics
        st.subheader("📊 Metrics")
        st.json(metrics)

        # Plot
        st.subheader("📈 Close Price + Rolling Mean")

        st.line_chart(df[["close", "rolling_mean"]])

        # Signal distribution
        st.subheader("📊 Signal Distribution")
        st.bar_chart(df["signal"].value_counts())

        # Data preview
        st.subheader("📄 Data Preview")
        st.dataframe(df.head(50))

    except Exception as e:
        st.error(f"Error: {str(e)}")

else:
    st.info("Upload a CSV file to begin")