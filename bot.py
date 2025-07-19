import requests
import pandas as pd
import yfinance as yf
import time
from ta.momentum import RSIIndicator

# === CONFIG ===
TELEGRAM_TOKEN = '8146407957:AAFtXKX-pyZex-VPYUWDDafyaKOaISJMCGY'
CHAT_ID = '6954984074'
SYMBOL = 'XAUUSD=X'  # Yahoo Finance symbol for Gold vs USD
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
CHECK_INTERVAL = 900  # 15 minutes

# === SEND MESSAGE TO TELEGRAM ===
def send_signal_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, json=payload)

# === FETCH AND ANALYZE RSI ===
def check_rsi_and_alert():
    df = yf.download(SYMBOL, period="2d", interval="15m")
    if df.empty:
        print("No data fetched.")
        return

    rsi = RSIIndicator(close=df['Close'], window=RSI_PERIOD).rsi()
    latest_rsi = rsi.iloc[-1]
    price = df['Close'].iloc[-1]

    print(f"RSI: {latest_rsi:.2f} | Price: {price:.2f}")

    if latest_rsi < RSI_OVERSOLD:
        message = f"📉 RSI SIGNAL: BUY XAUUSD\nRSI: {latest_rsi:.2f}\nPrice: {price:.2f}"
        send_signal_to_telegram(message)
    elif latest_rsi > RSI_OVERBOUGHT:
        message = f"📈 RSI SIGNAL: SELL XAUUSD\nRSI: {latest_rsi:.2f}\nPrice: {price:.2f}"
        send_signal_to_telegram(message)
    else:
        print("No signal.")

# === RUN LOOP ===
if __name__ == "__main__":
    while True:
        try:
            check_rsi_and_alert()
        except Exception as e:
            print("Error:", e)
        time.sleep(CHECK_INTERVAL)
