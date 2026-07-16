import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SSW_URL = "https://crypto-mcp-production-61ca.up.railway.app/ssw15m"

sent = set()


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


def check_signal():

    data = requests.get(
        SSW_URL,
        timeout=10
    ).json()

    signals = data.get("long", []) + data.get("short", [])

    for s in signals:

        key = (
            s["symbol"],
            s["signal"],
            s["entry"]
        )

        if key in sent:
            continue

        if s["confidence"] >= 0:

            msg = f"""
🚨 SSW SIGNAL

{s['signal']} {s['symbol']}

Entry: {s['entry']}
TP1: {s['tp1']}
TP2: {s['tp2']}
SL: {s['sl']}

Confidence: {s['confidence']}%
Risk: {s['risk']}
Quality: {s['entry_quality']}
"""

            send_message(msg)

            sent.add(key)



while True:

    try:
        check_signal()

    except Exception as e:
        print(e)

    time.sleep(300)
