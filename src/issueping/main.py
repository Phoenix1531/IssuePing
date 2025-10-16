from __future__ import annotations

import argparse
import logging
import re
from typing import Dict, Set

from dotenv import load_dotenv

from .config import load_config
from .github_client import GitHubClient
from .filters import is_assigned, is_pull_request
from .state import load_state, save_state
from .notifiers.telegram import telegram_enabled, send_telegram
from .notifiers.email_sendgrid import sendgrid_enabled, send_email


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("issueping")


IMAGE_PATTERN = re.compile(r'!\[.*?\]\((https?://[^\s)]+)\)')


def build_issue_key(repo_full_name: str, issue: Dict) -> str:
    number = issue.get("number")
    return f"{repo_full_name}#{number}"


def extract_first_image(issue: Dict) -> str | None:
    body = issue.get("body") or ""
    match = IMAGE_PATTERN.search(body)
    if match:
        url = match.group(1)
        if url.startswith(("http://", "https://")) and len(url) < 2000:
            return url
    return None


def notify(issue: Dict, dry_run: bool = False, verbose: bool = False) -> None:
    """Notify about an issue. In dry-run mode, print the message instead of sending."""
    image_url = extract_first_image(issue)

    repo_name = issue.get("repository_url", "").split("/repos/")[-1]
    title = issue.get("title") or "New issue"
    number = issue.get("number")
    html_url = issue.get("html_url") or ""
    labels = ", ".join(lbl.get("name", "") for lbl in (issue.get("labels") or [])) or "None"

    # Dry-run: print a human-friendly summary and return
    if dry_run:
        logger.info("DRY-RUN: would notify about issue")
        logger.info(f"Repo: {repo_name}")
        logger.info(f"Title: {title}")
        logger.info(f"Number: {number}")
        logger.info(f"Labels: {labels}")
        logger.info(f"URL: {html_url}")
        if image_url:
            logger.info(f"Image: {image_url}")
        return

    # Try both channels if configured
    if telegram_enabled():
        try:
            send_telegram(issue, image_url=image_url, verbose=verbose)
        except Exception as exc:
            logger.warning(f"Telegram notify failed: {exc}")

    if sendgrid_enabled():
        try:
            send_email(issue, image_url=image_url, verbose=verbose)
        except Exception as exc:
            logger.warning(f"SendGrid notify failed: {exc}")


def run(config_path: str | None = None, dry_run: bool = False, verbose: bool = False) -> None:
    """Main run loop. `config_path` defaults to config/repos.json if None."""
    cfg = load_config(config_path or "config/repos.json")
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
            notify(item, dry_run=dry_run, verbose=verbose)
            processed.add(issue_key)
            new_count += 1

    save_state(processed)
    logger.info(f"Done. New notifications: {new_count}")


def main(argv: list[str] | None = None) -> None:
    """CLI entrypoint used by console script. Loads .env then runs with parsed args."""
    parser = argparse.ArgumentParser(description="IssuePing: watch GitHub issues and notify")
    parser.add_argument("--config", "-c", help="Path to repos.json", default="config/repos.json")
    parser.add_argument("--dry-run", action="store_true", help="Print notifications instead of sending them")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose HTTP request/response logging")
    args = parser.parse_args(argv)

    # Load environment from .env if present (local testing convenience)
    load_dotenv()

    # Configure verbose logging for HTTP clients if requested
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        # Enable urllib3/request debug logs
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logging.getLogger("requests").setLevel(logging.DEBUG)

    run(config_path=args.config, dry_run=bool(args.dry_run), verbose=bool(args.verbose))


if __name__ == "__main__":
    main()


