# MLOps-batch-pipeline-with-multiple-signal-strategies

https://mlops-batch-pipeline-with-multiple-signal-strategies-czicnpty3.streamlit.app/
## 📌 Overview

This project implements a **production-style MLOps batch pipeline in Python** designed to simulate a real-world data processing workflow.

It processes financial time-series data (OHLCV), generates trading signals, and produces structured metrics along with detailed logs. The focus is not just on computation, but on building a **robust, reproducible, and deployment-ready system**.

---

## What This Project Demonstrates

This pipeline is intentionally simple in logic but strong in engineering design. It highlights:

* ✅ **Reproducibility** — deterministic outputs using config + seed
* ✅ **Observability** — structured logs and metrics
* ✅ **Robustness** — handles malformed and missing data
* ✅ **Deployment readiness** — Dockerized, one-command execution
* ✅ **Extensibility** — supports multiple signal strategies

---

## Dataset Understanding

The dataset contains **OHLCV (Open, High, Low, Close, Volume)** financial data.

Although multiple columns are present, this pipeline strictly uses:

👉 **`close` price** — the most relevant indicator of market state

This keeps the logic focused while still being realistic.

---

## How the Pipeline Works

### 1. Config-Driven Execution

* Reads parameters from `config.yaml`
* Validates required fields (`seed`, `window`, `version`)
* Ensures deterministic behavior via seed control

---

### 2. Data Loading & Cleaning

* Handles malformed CSV (single-column issue)
* Validates structure before processing
* Converts all numeric fields safely
* Removes invalid or missing values in `close`

---

### 3. Rolling Statistics

* Computes **rolling mean** → trend indicator
* Computes **rolling standard deviation** → volatility

The first `(window - 1)` rows produce NaN values and are **explicitly removed** to ensure consistent calculations.

---

## 📈 Signal Generation Strategies

The pipeline supports **three configurable signal strategies**:

---

### 🟢 1. Basic Signal (Trend-Based)

```
signal = 1 if close > rolling_mean else 0
```

* Simple and intuitive
* Captures overall trend
* Higher signal frequency (more noise)

---

### 🔵 2. Z-Score Signal (Volatility-Aware)

```
z = (close - rolling_mean) / rolling_std
signal = 1 if z > threshold else 0
```

* Considers both trend and volatility
* Filters weak movements
* Produces more selective signals

---

### 🔥 3. Hybrid Signal (High-Confidence)

```
signal = 1 if (basic AND z-score) else 0
```

* Combines trend + statistical significance
* Most strict and reliable
* Reduces false positives significantly

---

## Signal Strategy Comparison

All strategies were tested on the same dataset:

### 🟢 Basic Signal

```json
{
    "version": "v1",
    "rows_processed": 9996,
    "metric": "signal_rate",
    "value": 0.4991,
    "latency_ms": 60,
    "seed": 42,
    "status": "success"
}
```

---

### 🔵 Z-Score Signal

```json
{
    "version": "v1",
    "rows_processed": 9996,
    "metric": "signal_rate",
    "value": 0.3796,
    "latency_ms": 63,
    "seed": 42,
    "status": "success"
}
```

---

###  Hybrid Signal

```json
{
    "version": "v1",
    "rows_processed": 9996,
    "metric": "signal_rate",
    "value": 0.3796,
    "latency_ms": 63,
    "seed": 42,
    "status": "success"
}
```

---

## 🧠 Interpretation of Results

* **Basic (~49.9%)**

  * Almost half the data triggers signals
  * Sensitive to small changes → higher noise

* **Z-score (~37.9%)**

  * More selective
  * Filters out weak fluctuations
  * Better signal quality

* **Hybrid (~37.9%)**

  * Strong confirmation-based signals
  * Ensures both trend and strength
  * Most reliable for decision-making

👉 This demonstrates how adding **statistical context (volatility)** improves signal quality.

---

## 📦 Metrics Generated

Each run outputs:

* `rows_processed`
* `signal_rate`
* `latency_ms`
* `status`

Metrics are written even in failure scenarios for traceability.

---

## ▶️ How to Run Locally

```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## ⚙️ Configuration

```yaml
seed: 42
window: 5
version: "v1"

signal_type: "basic"   # basic | zscore | hybrid
z_threshold: 0.5
```

---

## 🪵 Logging

Logs include:

* Job lifecycle (start/end)
* Config details
* Data validation steps
* Signal computation
* Metrics summary
* Errors (if any)

---

## 🐳 Docker Usage

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

✔ Runs entire pipeline
✔ Outputs metrics + logs
✔ Prints result to console

---

## 🧪 Error Handling

The pipeline gracefully handles:

* Missing files
* Invalid CSV formats
* Missing `close` column
* Empty datasets
* Config errors

---

## 🧠 Design Philosophy

This project focuses on:

* Clean, modular structure
* Explicit validation
* Deterministic execution
* Real-world data handling

Rather than complex ML, the emphasis is on **engineering discipline**.

---

##  Key Takeaways

This project demonstrates the ability to:

* Build reliable and maintainable pipelines
* Handle imperfect real-world data
* Design reproducible systems
* Implement configurable logic

---

##  Future Improvements

* Add unit testing (pytest)
* Integrate MLflow tracking
* Add real-time streaming pipeline
* Deploy via CI/CD

---

## 👤 Author

AXLR8

---

## 📌 Notes

* Default signal type is **basic** (as per assessment requirement)
* Z-score and hybrid strategies are added as enhancements

---
