from __future__ import annotations

import os
from typing import Dict

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging


logger = logging.getLogger("issueping.email")


def sendgrid_enabled() -> bool:
    return bool(os.getenv("SENDGRID_API_KEY") and os.getenv("EMAIL_TO") and os.getenv("EMAIL_FROM"))

def send_email(issue: Dict, image_url: str | None = None, verbose: bool = False) -> None:
    """Send email notification for a new issue."""
    api_key = os.getenv("SENDGRID_API_KEY")
    email_to = os.getenv("EMAIL_TO")
    email_from = os.getenv("EMAIL_FROM")
    if not api_key or not email_to or not email_from:
        return


    title = issue.get("title") or "New issue"
    number = issue.get("number")
    html_url = issue.get("html_url") or ""
    repo = issue.get("repository_url", "").split("/repos/")[-1]
    labels = ", ".join(lbl.get("name", "") for lbl in (issue.get("labels") or [])) or "None"


    subject = f"🔔 New issue in {repo}: {title}"


    html_content = f"""
        <div style="font-family: Arial, sans-serif; line-height:1.6; padding:10px;">
        <h2 style="margin-bottom:5px;">New GitHub Issue 📌</h2>
        <p><strong>Repository:</strong> {repo}</p>
        <p><strong>Title:</strong> {title}</p>
        <p><strong>Labels:</strong> {labels}</p>
        <p><a href="{html_url}" style="color:#2d89ef; text-decoration:none; font-weight:bold;">
        🔗 View Issue on GitHub
        </a></p>
        """


    # If an image is present, embed it below the details
    if image_url:
        html_content += f"""
        <div style="margin-top:15px;">
        <p><strong>Image from Issue:</strong></p>
        <img src="{image_url}" alt="Issue image" style="max-width:500px; border:1px solid #ddd; border-radius:6px;" />
        </div>
        """


    html_content += "</div>"


    message = Mail(
        from_email=email_from,
        to_emails=email_to,
        subject=subject,
        plain_text_content=f"{title} - {html_url}", # fallback text-only
        html_content=html_content,
        )


    try:
        sg = SendGridAPIClient(api_key)
        if verbose:
            logger.info("[sendgrid] sending message")
        response = sg.send(message)
        if verbose:
            logger.info(f"[sendgrid] status_code={getattr(response, 'status_code', None)}")
            try:
                logger.info(f"[sendgrid] body={getattr(response, 'body', None)}")
            except Exception:
                pass
        return response
    except Exception as e:
        logger.error(f"SendGrid email failed: {e}")
        raise  # Re-raise to be caught by main.py


