import pandas as pd
import requests
import os
import json

# ================= CONFIG =================

INDICES = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "SENSEX": "^BSESN"
}

REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# ================= RSI =================

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ================= DATA FETCH =================
# Source: Stooq (indices ARE available, stocks are not)

def fetch_index(symbol):
    url = f"https://stooq.pl/q/d/l/?s={sym
