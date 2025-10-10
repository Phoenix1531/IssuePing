from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class RepoConfig:
    name: str
    labels: List[str]


@dataclass(frozen=True)
class AppConfig:
    repos: List[RepoConfig]


def load_config(config_path: str | Path = "config/repos.json") -> AppConfig:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path}")
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    repos: List[RepoConfig] = []
    for item in raw.get("repos", []):
        name = str(item.get("name", "")).strip()
        labels = [str(lbl).strip() for lbl in item.get("labels", []) if str(lbl).strip()]
        if not name:
            continue
        repos.append(RepoConfig(name=name, labels=labels))
    return AppConfig(repos=repos)


