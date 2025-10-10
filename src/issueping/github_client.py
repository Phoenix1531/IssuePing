from __future__ import annotations

import os
from typing import Dict, Generator, Iterable, List, Optional

import requests


class GitHubClient:
    """Minimal GitHub REST API client for listing issues by label.

    Uses the Actions-provided GITHUB_TOKEN when available, falling back to
    the environment if set locally.
    """

    def __init__(self, token: Optional[str] = None) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        self.session = requests.Session()
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "issueping-bot",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.session.headers.update(headers)

    def list_issues(self, repo_full_name: str, labels: Iterable[str]) -> Generator[Dict, None, None]:
        """Yield open issues from `owner/repo` filtered by labels.

        Excludes PRs and supports pagination (100 per page).
        """
        owner_repo = repo_full_name.strip()
        params = {
            "state": "open",
            "labels": ",".join(lbl for lbl in labels if lbl),
            "per_page": 100,
        }
        url = f"https://api.github.com/repos/{owner_repo}/issues"
        while url:
            resp = self.session.get(url, params=params)
            params = {}  # only for first request
            resp.raise_for_status()
            items: List[Dict] = resp.json()
            for item in items:
                yield item
            url = _parse_next_link(resp.headers.get("Link"))


def _parse_next_link(link_header: Optional[str]) -> Optional[str]:
    if not link_header:
        return None
    # Link: <url1>; rel="next", <url2>; rel="last"
    parts = [p.strip() for p in link_header.split(",")]
    for part in parts:
        if "rel=\"next\"" in part:
            start = part.find("<")
            end = part.find(">", start + 1)
            if start != -1 and end != -1:
                return part[start + 1 : end]
    return None


