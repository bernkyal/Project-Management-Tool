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

# WHITE-BOX (Branch Testing): forces internal save-failure branch to confirm correct error handling path.
def test_create_project_returns_error_if_save_fails(data_file, monkeypatch):
    def fake_save(_projects):
        return False, "disk error"

    monkeypatch.setattr(core, "save_projects", fake_save)

    resp = core.create_project("X", "Y")
    assert resp["success"] is False
    assert "disk error" in resp["message"].lower()

