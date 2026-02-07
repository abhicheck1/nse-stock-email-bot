import pandas as pd
import requests
import os
import json

# ================= CONFIG =================

NSE_STOCKS = {
    "RELIANCE": "reliance.ns",
    "TCS": "tcs.ns",
    "INFY": "infy.ns",
    "HDFCBANK": "hdfcbank.ns",
    "ICICIBANK": "icicibank.ns"
}

REPO = os.getenv("GITHUB_REPOSITORY")  # owner/repo
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# ================= INDICATOR =================

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ================= DATA FETCH =================

def fetch_stock(symbol):
    url = f"https://stooq.pl/q/d/l/?s={symbol}&i=d"
    df = pd.read_csv(url)

    if df.empty or "Close" not in df.columns:
        return None

    df["Close"] = df["Close"].astype(float)
    return df

# ================= ANALYSIS =================

def analyze_market():
    report = []

    for name, symbol in NSE_STOCKS.items():
        df = fetch_stock(symbol)

        if df is None or len(df) < 30:
            continue

        close = df["Close"]
        price = close.iloc[-1]
        rsi_val = rsi(close).iloc[-1]

        signal = "HOLD"
        if rsi_val < 35:
            signal = "BUY"
        elif rsi_val > 65:
            signal = "SELL"

        report.append(
            f"### {name}\n"
            f"- Price: ₹{price:.2f}\n"
            f"- RSI: {rsi_val:.2f}\n"
            f"- Signal: **{signal}**\n"
        )

    if not report:
        return "NSE bot ran successfully, but no data was returned."

    return "## 📈 NSE Daily Stock Report\n\n" + "\n".join(report)

# ================= GITHUB ISSUE =================

def create_github_issue(content):
    url = f"https://api.github.com/repos/{REPO}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "title": "NSE Daily Stock Update",
        "body": content
    }
    requests.post(url, headers=headers, data=json.dumps(payload))

# ================= MAIN =================

if __name__ == "__main__":
    result = analyze_market()
    print(result)
    create_github_issue(result)
