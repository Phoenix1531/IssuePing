from __future__ import annotations

import os
from typing import Dict, Optional

import requests


def telegram_enabled() -> bool:
    return bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))


def send_telegram(issue: Dict, image_url: str | None = None, verbose: bool = False) -> None:
    """Send Telegram notification for a new issue."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return

    repo_name = "/".join(issue['repository_url'].split('/')[-2:])
    title = issue['title'].replace('_', '\\_').replace('*', '\\*').replace('[', '\\[')
    text = f"🟢 New Issue in {repo_name}\n" \
           f"#{issue['number']}: {title}\n" \
           f"{issue['html_url']}"



    if image_url:
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        payload = {
            "chat_id": chat_id,
            "photo": image_url,
            "caption": text,
            "parse_mode": "Markdown"
        }
    else:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }

    if verbose:
        # print request details
        print(f"[telegram] POST {url}")
        print(f"[telegram] payload: {payload}")

    resp = requests.post(url, json=payload, timeout=30)

    if verbose:
        print(f"[telegram] status: {resp.status_code}")
        try:
            print(f"[telegram] response: {resp.json()}")
        except Exception:
            print(f"[telegram] response text: {resp.text}")

    resp.raise_for_status()


