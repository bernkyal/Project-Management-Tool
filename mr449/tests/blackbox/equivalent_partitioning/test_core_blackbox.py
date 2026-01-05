import re
from datetime import datetime, timedelta
import pytest
import project_tool.core as core
import project_tool.persistence as persistence
from project_tool.models import Project

@pytest.fixture()
def data_file(tmp_path, monkeypatch):
    test_file = tmp_path / "projects.json"

    def _load_projects():
        return persistence.load_projects(path=str(test_file))

    def _save_projects(projects):
        return persistence.save_projects(projects, path=str(test_file))

    monkeypatch.setattr(core, "load_projects", _load_projects)
    monkeypatch.setattr(core, "save_projects", _save_projects)

    return str(test_file)

def _seed_projects(path, projects):
    ok, msg = persistence.save_projects(projects, path=path)
    assert ok is True, msg

# create project tests
# BLACK-BOX (Equivalent Partitioning): input class {empty} must be rejected with clear error message.
def test_create_project_rejects_empty_title(data_file):
    resp = core.create_project("")
    assert resp["success"] is False
    assert "cannot be empty" in resp["message"].lower()

# BLACK-BOX (Equivalent Partitioning): input class {whitespace-only} must be rejected (same class as empty after trimming).
def test_create_project_rejects_whitespace_title(data_file):
    resp = core.create_project("   ")
    assert resp["success"] is False
    assert "cannot be empty" in resp["message"].lower()

# BLACK-BOX (Equivalent Partitioning): input class {duplicate title ignoring case} must be rejected to enforce uniqueness.
def test_create_project_rejects_duplicate_title_case_insensitive(data_file):
    _seed_projects(data_file, [Project(project_id="P-111111", title="My Title")])

    resp = core.create_project("my title", "desc")
    assert resp["success"] is False
    assert "already exists" in resp["message"].lower()

# filer each of the projects
# BLACK-BOX (Equivalent Partitioning): partitions projects into {Active} vs {Non-active} and expects only Active returned.
def test_get_active_projects_returns_only_active(data_file):
    _seed_projects(
        data_file,
        [
            Project(project_id="P-1", title="A", status="Active"),
            Project(project_id="P-2", title="B", status="Planning"),
            Project(project_id="P-3", title="C", status="Active"),
        ],
    )

    active = core.get_active_projects()
    assert [p.project_id for p in active] == ["P-1", "P-3"]

# BLACK-BOX (Equivalent Partitioning): given a status input, returned set should include only those in that status class.
def test_filter_projects_by_status(data_file):
    _seed_projects(
        data_file,
        [
            Project(project_id="P-1", title="A", status="On Hold"),
            Project(project_id="P-2", title="B", status="Planning"),
        ],
    )

    on_hold = core.filter_projects_by_status("On Hold")
    assert len(on_hold) == 1
    assert on_hold[0].project_id == "P-1"
