import json
import os
import pytest
from project_tool.models import Project
from project_tool.persistence import load_projects, save_projects

import project_tool.persistence as persistence
import project_tool.deletion as deletion

@pytest.fixture()
def storage_paths(tmp_path, monkeypatch):
    projects_file = tmp_path / "projects.json"
    deleted_log = tmp_path / "deleted_projects.json"

    monkeypatch.setattr(deletion, "DELETED_LOG_FILE", str(deleted_log))

    def _load_projects():
        return persistence.load_projects(path=str(projects_file))

    def _save_projects(projects):
        return persistence.save_projects(projects, path=str(projects_file))

    monkeypatch.setattr(deletion, "load_projects", _load_projects)
    monkeypatch.setattr(deletion, "save_projects", _save_projects)

    return str(projects_file), str(deleted_log)


def _seed_projects(path, projects):
    ok, msg = save_projects(projects, path=path)
    assert ok is True, msg

# show all the project ids
# BLACK-BOX (Equivalent Partitioning): partition {no projects in storage} should return empty ID list.
def test_list_project_ids_empty(storage_paths):
    projects_file, _ = storage_paths
    _seed_projects(projects_file, [])
    assert deletion.list_project_ids() == []

# BLACK-BOX (Equivalent Partitioning): partition {projects exist} should return the correct ordered ID list.
def test_list_project_ids_returns_ids(storage_paths):
    projects_file, _ = storage_paths
    _seed_projects(
        projects_file,
        [
            Project(project_id="P-AAAAAA", title="Alpha"),
            Project(project_id="P-BBBBBB", title="Beta"),
        ],
    )

    ids = deletion.list_project_ids()
    assert ids == ["P-AAAAAA", "P-BBBBBB"]


# input validations
# BLACK-BOX (Equivalent Partitioning): invalid ID class {empty} must be rejected with clear message.
def test_delete_project_by_id_rejects_empty_id(storage_paths):
    resp = deletion.delete_project_by_id("", confirm=True)
    assert resp["success"] is False
    assert "must be provided" in resp["message"].lower()

# BLACK-BOX (Equivalent Partitioning): invalid ID class {bad format} must be rejected.
def test_delete_project_by_id_rejects_invalid_format(storage_paths):
    resp = deletion.delete_project_by_id("NOT-A-PROJECT", confirm=True)
    assert resp["success"] is False
    assert "format is invalid" in resp["message"].lower()

# delete project id and it's effects
# BLACK-BOX (Equivalent Partitioning): ID class {well-formed but not present} must return not found and not create log.
def test_delete_project_by_id_not_found(storage_paths):
    projects_file, deleted_log = storage_paths
    _seed_projects(projects_file, [Project(project_id="P-AAAAAA", title="Alpha")])

    resp = deletion.delete_project_by_id("P-NOTREAL", confirm=True)
    assert resp["success"] is False
    assert "not found" in resp["message"].lower()

    # deleted log shouldn't exist once it has failed
    assert not os.path.exists(deleted_log)


# BLACK-BOX (Equivalent Partitioning): valid ID format class {numeric P123} should be accepted and logged correctly.
def test_delete_project_by_id_accepts_numeric_format(storage_paths):
    projects_file, deleted_log = storage_paths

    _seed_projects(projects_file, [Project(project_id="P123", title="Numeric")])

    resp = deletion.delete_project_by_id("P123", confirm=True)
    assert resp["success"] is True

    with open(deleted_log, "r", encoding="utf-8") as f:
        raw = json.load(f)

    assert raw[-1]["project_id"] == "P123"


