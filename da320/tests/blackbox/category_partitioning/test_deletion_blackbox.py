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


# BLACK-BOX (Category Partition Method): category "confirmation" with choice {False} must block deletion.
def test_delete_project_by_id_requires_confirmation(storage_paths):
    resp = deletion.delete_project_by_id("P-AAAAAA", confirm=False)
    assert resp["success"] is False
    assert "requires confirmation" in resp["message"].lower()


# BLACK-BOX (Category Partition Method): validates the full delete functional unit incl. persistence and deletion logging effects.
def test_delete_project_by_id_success_removes_project_and_logs(storage_paths):
    projects_file, deleted_log = storage_paths

    _seed_projects(
        projects_file,
        [
            Project(project_id="P-AAAAAA", title="Alpha"),
            Project(project_id="P-BBBBBB", title="Beta"),
        ],
    )

    resp = deletion.delete_project_by_id("P-AAAAAA", confirm=True)
    assert resp["success"] is True
    assert "deleted successfully" in resp["message"].lower()

    # Project removed from projects storage
    projects, msg = load_projects(path=projects_file)
    assert msg in ("", None)
    assert [p.project_id for p in projects] == ["P-BBBBBB"]

    # Deleted log file created and contains deleted id
    with open(deleted_log, "r", encoding="utf-8") as f:
        raw = json.load(f)

    assert isinstance(raw, list)
    assert raw[-1]["project_id"] == "P-AAAAAA"


