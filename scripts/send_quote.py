import json
import random
import requests
from pathlib import Path

WEBHOOK_URL = "https://chat.hftisa.ir/hooks/hag9xxbudffatkg5cx7m14fqna"
API_URL = "https://api.majidapi.ir/fun/angizeshi?token=tn5iihsbzma2e0l:QT8N1OPN6Uk4AzdouhzT"

FALLBACK_FILE = Path("quotes.txt")

def load_fallback_quotes():
    if not FALLBACK_FILE.exists():
        return [
            "امروز یک فرصت تازه برای ساختن چیزهای بهتر است.",
            "شروع کن؛ انگیزه معمولاً بعد از حرکت می آید نه قبل از آن.",
            "پیشرفت کوچک روزانه، نتیجه بزرگ ماهانه می سازد.",
        ]

    with FALLBACK_FILE.open("r", encoding="utf-8") as f:
        quotes = [line.strip() for line in f if line.strip()]
    return quotes or [
        "امروز یک فرصت تازه برای ساختن چیزهای بهتر است."
    ]

def get_quote_from_api():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == 200:
            text = data.get("result", "").strip()
            if text:
                return text, "majidapi"
    except Exception as exc:
        print(f"API failed: {exc}")

    return None, None

def get_quote():
    text, source = get_quote_from_api()
    if text:
        return text, source

    quotes = load_fallback_quotes()
    return random.choice(quotes), "fallback"

def send_to_mattermost(text, source):
    payload = {
        "username": "Motivation Bot",
        "text": (
            "صبح بخیر تیم ☀️\n\n"
            f"> {text}\n\n"
            f"_source: {source}_"
        ),
    }

    response = requests.post(
        WEBHOOK_URL,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    response.raise_for_status()

def main():
    text, source = get_quote()
    send_to_mattermost(text, source)
    print("Quote sent successfully")

if __name__ == "__main__":
    main()

