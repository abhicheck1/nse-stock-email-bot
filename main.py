import pandas as pd
import requests
import smtplib
from email.mime.text import MIMEText

# ================= CONFIG =================

NSE_STOCKS = {
    "RELIANCE": "reliance.ns",
    "TCS": "tcs.ns",
    "INFY": "infy.ns",
    "HDFCBANK": "hdfcbank.ns",
    "ICICIBANK": "icicibank.ns"
}

EMAIL_ADDRESS = "YOUR_EMAIL@gmail.com"
EMAIL_PASSWORD = "YOUR_GMAIL_APP_PASSWORD"
EMAIL_RECEIVER = "RECEIVER_EMAIL@gmail.com"

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
            f"{name}\nPrice: ₹{price:.2f}\nRSI: {rsi_val:.2f}\nSignal: {signal}\n"
        )

    if not report:
        return "NSE bot ran successfully, but no data was returned."

    return "📈 NSE DAILY STOCK REPORT\n\n" + "\n".join(report)

# ================= EMAIL =================

def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "NSE Daily Stock Report"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

# ================= MAIN =================

if __name__ == "__main__":
    result = analyze_market()
    print(result)
    send_email(result)
