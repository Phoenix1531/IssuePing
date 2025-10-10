from __future__ import annotations

import os
from typing import Dict

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def sendgrid_enabled() -> bool:
    return bool(os.getenv("SENDGRID_API_KEY") and os.getenv("EMAIL_TO") and os.getenv("EMAIL_FROM"))


def send_email(issue: Dict) -> None:
    api_key = os.getenv("SENDGRID_API_KEY")
    email_to = os.getenv("EMAIL_TO")
    email_from = os.getenv("EMAIL_FROM")
    if not api_key or not email_to or not email_from:
        return

    title = issue.get("title") or "New issue"
    number = issue.get("number")
    html_url = issue.get("html_url") or ""
    repo = issue.get("repository_url", "").split("/repos/")[-1]
    labels = ", ".join(lbl.get("name", "") for lbl in (issue.get("labels") or []))

    subject = f"New issue in {repo}: {title}"
    body = (
        f"Repo: {repo}\n"
        f"Title: {title}\n"
        f"Labels: {labels}\n\n"
        f"Link: {html_url}"
    )

    message = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject=subject,
        plain_text_content=body,
    )
    sg = SendGridAPIClient(api_key)
    sg.send(message)


