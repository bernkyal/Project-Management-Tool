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

# WHITE-BOX (Loop Testing): exercises repeated deletion actions to ensure append logic works across multiple iterations.
def test_deleted_log_appends_multiple_deletions(storage_paths):
    projects_file, deleted_log = storage_paths

    _seed_projects(
        projects_file,
        [
            Project(project_id="P-AAAAAA", title="Alpha"),
            Project(project_id="P-BBBBBB", title="Beta"),
        ],
    )

    resp1 = deletion.delete_project_by_id("P-AAAAAA", confirm=True)
    resp2 = deletion.delete_project_by_id("P-BBBBBB", confirm=True)

    assert resp1["success"] is True
    assert resp2["success"] is True

    with open(deleted_log, "r", encoding="utf-8") as f:
        raw = json.load(f)

    assert [x["project_id"] for x in raw] == ["P-AAAAAA", "P-BBBBBB"]
