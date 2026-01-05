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

# BLACK-BOX (Category Partition Method): validates a full "create project" functional unit incl. defaults & persistence effects.
def test_create_project_success_persists_and_sets_defaults(data_file):
    resp = core.create_project("New Project", "Desc")
    assert resp["success"] is True
    assert "created successfully" in resp["message"].lower()

    projects, msg = persistence.load_projects(path=data_file)
    assert msg in ("", None, "")
    assert len(projects) == 1

    p = projects[0]
    assert p.title == "New Project"
    assert p.description == "Desc"
    assert p.status == "Planning"
    assert p.project_id.startswith("P-")
    assert re.fullmatch(r"P-[A-F0-9]{6}", p.project_id) is not None
