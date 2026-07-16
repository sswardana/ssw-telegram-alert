import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("BOT_TOKEN atau CHAT_ID belum diset.")

SSW_URL = "https://crypto-mcp-production-61ca.up.railway.app/ssw15m"

sent = {}
COOLDOWN = 1800  # 30 menit


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            },
            timeout=10
        )
    except Exception as e:
        print(f"Telegram Error: {e}")


def check_signal():

    response = requests.get(
        SSW_URL,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    signals = data.get("long", []) + data.get("short", [])

    for s in signals:

        key = f"{s['symbol']}_{s['signal']}"
        now = time.time()

        if key in sent and (now - sent[key] < COOLDOWN):
            continue

        if s["confidence"] >= 70:

            msg = f"""
🚨 <b>SSW SCALPING SIGNAL</b>

{'🟢' if s['signal'] == 'LONG' else '🔴'} <b>{s['signal']} {s['symbol']}</b>

━━━━━━━━━━━━━━━━

💰 <b>Entry</b> : {s['entry']}

🎯 <b>TP1</b> : {s['tp1']}
🎯 <b>TP2</b> : {s['tp2']}

🛑 <b>SL</b> : {s['sl']}

━━━━━━━━━━━━━━━━

📊 <b>Confidence</b> : {s['confidence']}%
⚠️ <b>Risk</b> : {s.get('risk', 'UNKNOWN')}
⭐ <b>Quality</b> : {s.get('entry_quality', 'N/A')}

📈 <a href="https://www.tradingview.com/chart/?symbol=BINANCE:{s['symbol']}">Open TradingView</a>
"""

            send_message(msg)

            sent[key] = now


while True:

    try:
        check_signal()

    except Exception as e:
        print(e)

    time.sleep(300)
