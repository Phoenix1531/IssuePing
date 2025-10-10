from __future__ import annotations

from typing import Dict


def is_pull_request(item: Dict) -> bool:
    return "pull_request" in item


def is_assigned(item: Dict) -> bool:
    # GitHub REST: `assignee` single or `assignees` list
    if item.get("assignee"):
        return True
    assignees = item.get("assignees") or []
    return bool(assignees)


