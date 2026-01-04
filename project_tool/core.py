from __future__ import annotations

from datetime import datetime
from typing import List, Optional
import uuid

from project_tool.models import Project
from project_tool.persistence import load_projects, save_projects
from project_tool.responses import (
    success,
    error,
    project_created,
    project_updated,
    project_not_found,
    invalid_input,
)


def _find_project(projects: List[Project], project_id: str) -> Optional[Project]:
    for p in projects:
        if p.project_id == project_id:
            return p
    return None


# M1, M2, M3, M4
# Create project

def create_project(title: str, description: str = ""):
    """
    M1: generate unique project ID
    M2: set initial status
    M3: prevent empty project name
    M4: confirmation after creation
    """
    if not title or not title.strip():
        return invalid_input("Project title cannot be empty.")

    projects, _ = load_projects()

    # A6 / M3: prevent duplicate titles
    for p in projects:
        if p.title.lower() == title.lower():
            return invalid_input("A project with this title already exists.")

    project_id = f"P-{uuid.uuid4().hex[:6].upper()}"

    project = Project(
        project_id=project_id,
        title=title.strip(),
        description=description.strip(),
        status="Planning",
    )

    projects.append(project)
    ok, msg = save_projects(projects)

    if not ok:
        return error(msg)

    return project_created(project_id)


# A1, A6
# Update project title

def update_project_title(project_id: str, new_title: str):
    if not new_title or not new_title.strip():
        return invalid_input("Project title cannot be empty.")

    projects, _ = load_projects()
    project = _find_project(projects, project_id)

    if not project:
        return project_not_found(project_id)

    for p in projects:
        if p.project_id != project_id and p.title.lower() == new_title.lower():
            return invalid_input("Another project already uses this title.")

    project.title = new_title.strip()
    save_projects(projects)

    return project_updated(project_id, "title")
