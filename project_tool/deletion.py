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
    # Not yet incorporated _log_deleted_project, somebody elses user story!
    _log_deleted_project(project_id) 

    return project_deleted(project_id)