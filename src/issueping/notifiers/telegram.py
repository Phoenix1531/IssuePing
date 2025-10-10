from __future__ import annotations

import os
from typing import Dict, Optional

import requests


def telegram_enabled() -> bool:
    return bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))


def send_telegram(issue: Dict) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    title = issue.get("title") or "New issue"
    number = issue.get("number")
    html_url = issue.get("html_url") or ""
    repo = issue.get("repository_url", "").split("/repos/")[-1]
    labels = ", ".join(lbl.get("name", "") for lbl in (issue.get("labels") or []))

    text = (
        f"[{repo}] New issue: {title} (#{number})\n"
        f"Labels: {labels}\n{html_url}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    })
    resp.raise_for_status()


