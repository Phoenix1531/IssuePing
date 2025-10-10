from __future__ import annotations

import json
from pathlib import Path
from typing import Set


STATE_DIR = Path(".issueping_cache")
STATE_FILE = STATE_DIR / "state.json"


def load_state() -> Set[str]:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        return set()
    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return set(str(x) for x in data)
        return set()
    except Exception:
        # Corrupt cache should not crash the run
        return set()


def save_state(processed: Set[str]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(sorted(processed), f, indent=2)


