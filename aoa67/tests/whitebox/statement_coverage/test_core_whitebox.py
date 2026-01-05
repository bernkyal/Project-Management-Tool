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

# WHITE-BOX (Statement Testing): verifies internal history append statement executes when status changes.
def test_update_project_status_success_records_history(data_file):
    _seed_projects(data_file, [Project(project_id="P-AAAAAA", title="Alpha")])

    resp = core.update_project_status("P-AAAAAA", "Active")
    assert resp["success"] is True

    projects, _ = persistence.load_projects(path=data_file)
    p = projects[0]
    assert p.status == "Active"
    assert len(p.status_history) == 1
    assert p.status_history[0]["status"] == "Active"
    assert "timestamp" in p.status_history[0]
