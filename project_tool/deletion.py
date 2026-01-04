from __future__ import annotations

import re
import json
import os
from typing import List

from project_tool.persistence import load_projects, save_projects
from project_tool.responses import (
    project_deleted,
    project_not_found,
    invalid_input,
    success,
)


DELETED_LOG_FILE = os.path.join("data", "deleted_projects.json")


def _ensure_deleted_log_exists() -> None:
    folder = os.path.dirname(DELETED_LOG_FILE)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(DELETED_LOG_FILE):
        with open(DELETED_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def _log_deleted_project(project_id: str) -> None:

# D8: keep a record of deleted projects.

    _ensure_deleted_log_exists()

    with open(DELETED_LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append({"project_id": project_id})

    with open(DELETED_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# D5
# List project IDs

def list_project_ids() -> List[str]:
    projects, _ = load_projects()
    return [p.project_id for p in projects]


# D1–D7, D9
# Delete project

def delete_project_by_id(project_id: str, confirm: bool = False):

    if not project_id or not project_id.strip():
        return invalid_input("Project ID must be provided.")

    if not re.fullmatch(r"P\d+|P-[A-Za-z0-9]+", project_id):
        return invalid_input("Project ID format is invalid.")

    if not confirm:
        return invalid_input("Deletion requires confirmation.")

    projects, _ = load_projects()

    remaining = []
    found = False

    for p in projects:
        if p.project_id == project_id:
            found = True
        else:
            remaining.append(p)

    if not found:
        return project_not_found(project_id)

    save_projects(remaining)
    _log_deleted_project(project_id)

    return project_deleted(project_id)
