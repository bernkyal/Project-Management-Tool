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


# BLACK-BOX (Boundary Value Analysis): boundary around "today" — date just before today must be rejected.
def test_update_project_deadline_rejects_past_date(data_file):
    past = (datetime.now().date() - timedelta(days=1)).isoformat()
    resp = core.update_project_deadline("P-AAAAAA", past)
    assert resp["success"] is False
    assert "past" in resp["message"].lower()


# BLACK-BOX (Boundary Value Analysis): boundary around "today" — valid future date just beyond today should be accepted.
def test_update_project_deadline_success(data_file):
    _seed_projects(data_file, [Project(project_id="P-AAAAAA", title="Alpha")])

    future = (datetime.now().date() + timedelta(days=10)).isoformat()
    resp = core.update_project_deadline("P-AAAAAA", future)
    assert resp["success"] is True

    projects, _ = persistence.load_projects(path=data_file)
    assert projects[0].deadline == future
