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

def load_projects(path: str = DEFAULT_DATA_FILE) -> Tuple[List[Project], str]:

# B1, B2, B4:

    ensure_data_file_exists(path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        if raw is None:
            return [], "projects.json was empty; starting with no projects."

        if not isinstance(raw, list):
            return [], "projects.json format is invalid (expected a list). Starting empty."

        projects = [Project.from_dict(item) for item in raw]
        return projects, ""

    except json.JSONDecodeError:
        # B4: corrupted JSON - recover by resetting to []
        with _file_lock:
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        return [], "projects.json was corrupted. It has been reset to an empty list."

    except OSError as e:
        return [], f"Could not read projects file: {e}"


def save_projects(projects: List[Project], path: str = DEFAULT_DATA_FILE) -> Tuple[bool, str]:

#B5, B6, B8, B9:

    ensure_data_file_exists(path)

    ok, msg = validate_before_save(projects)
    if not ok:
        return False, msg

    data = [p.to_dict() for p in projects]

    # Write safely: lock + temp file + replace
    with _file_lock:
        temp_path = f"{path}.tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_path, path)
            return True, ""

        except OSError as e:
            return False, f"Could not save projects file: {e}"


# Autosave (B7)

def start_autosave(get_projects_func, interval_seconds: int = 30, path: str = DEFAULT_DATA_FILE) -> None:

    global _autosave_thread

    if _autosave_thread and _autosave_thread.is_alive():
        return  # already running

    _autosave_stop_event.clear()

    def _worker():
        while not _autosave_stop_event.is_set():
            time.sleep(interval_seconds)
            projects = get_projects_func()
            save_projects(projects, path=path)

    _autosave_thread = threading.Thread(target=_worker, daemon=True)
    _autosave_thread.start()


def stop_autosave() -> None:

    _autosave_stop_event.set()



