from __future__ import annotations

import logging
from typing import Dict, Set

from .config import load_config
from .github_client import GitHubClient
from .filters import is_assigned, is_pull_request
from .state import load_state, save_state
from .notifiers.telegram import telegram_enabled, send_telegram
from .notifiers.email_sendgrid import sendgrid_enabled, send_email


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("issueping")


def run() -> None:
    cfg = load_config()
    client = GitHubClient()
    processed: Set[str] = load_state()
    new_count = 0

    for repo in cfg.repos:
        logger.info(f"Checking {repo.name} with labels {repo.labels}...")
        for item in client.list_issues(repo.name, repo.labels):
            if is_pull_request(item):
                continue
            if is_assigned(item):
                continue
            issue_key = build_issue_key(repo.name, item)
            if issue_key in processed:
                continue
            notify(item)
            processed.add(issue_key)
            new_count += 1

    save_state(processed)
    logger.info(f"Done. New notifications: {new_count}")


def build_issue_key(repo_full_name: str, issue: Dict) -> str:
    number = issue.get("number")
    return f"{repo_full_name}#{number}"


def notify(issue: Dict) -> None:
    # Try both channels if configured
    if telegram_enabled():
        try:
            send_telegram(issue)
        except Exception as exc:
            logger.warning(f"Telegram notify failed: {exc}")
    if sendgrid_enabled():
        try:
            send_email(issue)
        except Exception as exc:
            logger.warning(f"SendGrid notify failed: {exc}")


