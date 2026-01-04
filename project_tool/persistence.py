from __future__ import annotations

import json
import os
import threading
import time
from typing import List, Tuple, Optional

from project_tool.models import Project


DEFAULT_DATA_FILE = os.path.join("data", "projects.json")

# B9: prevent simultaneous writes
_file_lock = threading.Lock()

# B7: autosave control
_autosave_thread: Optional[threading.Thread] = None
_autosave_stop_event = threading.Event()



def ensure_data_file_exists(path: str = DEFAULT_DATA_FILE) -> None:

    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def validate_before_save(projects: List[Project]) -> Tuple[bool, str]:

    # B8

    ids = set()
    for p in projects:
        if not p.project_id:
            return False, "A project is missing a project_id."
        if not p.title or not p.title.strip():
            return False, f"Project {p.project_id} has an empty title."
        if p.project_id in ids:
            return False, f"Duplicate project_id found: {p.project_id}"
        ids.add(p.project_id)

    return True, ""



