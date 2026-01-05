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

# update and alter the projects
# BLACK-BOX (Equivalent Partitioning): input class {empty/whitespace new title} must be rejected.
def test_update_project_title_rejects_empty_title(data_file):
    resp = core.update_project_title("P-111111", "   ")
    assert resp["success"] is False
    assert "cannot be empty" in resp["message"].lower()

# BLACK-BOX (Equivalent Partitioning): input class {non-existent project ID} must produce "not found" response.
def test_update_project_title_not_found(data_file):
    resp = core.update_project_title("P-NOTREAL", "New")
    assert resp["success"] is False
    assert "not found" in resp["message"].lower()

# BLACK-BOX (Equivalent Partitioning): input class {new title duplicates another project's title} must be rejected.
def test_update_project_title_rejects_duplicate_title(data_file):
    _seed_projects(
        data_file,
        [
            Project(project_id="P-AAAAAA", title="Alpha"),
            Project(project_id="P-BBBBBB", title="Beta"),
        ],
    )

    resp = core.update_project_title("P-AAAAAA", "beta")
    assert resp["success"] is False
    assert "already uses this title" in resp["message"].lower()

 # BLACK-BOX (Equivalent Partitioning): valid update class should succeed and persist title change.
def test_update_project_title_success(data_file):
    _seed_projects(data_file, [Project(project_id="P-AAAAAA", title="Alpha")])

    resp = core.update_project_title("P-AAAAAA", "New Alpha")
    assert resp["success"] is True
    assert "updated" in resp["message"].lower()

    projects, _ = persistence.load_projects(path=data_file)
    assert len(projects) == 1
    assert projects[0].title == "New Alpha"


#project descriptions
# BLACK-BOX (Equivalent Partitioning): invalid ID class should return not found for description update.
def test_update_project_description_not_found(data_file):
    resp = core.update_project_description("P-NOTREAL", "Desc")
    assert resp["success"] is False
    assert "not found" in resp["message"].lower()

# BLACK-BOX (Equivalent Partitioning): valid description update class should persist the new description.
def test_update_project_description_success(data_file):
    _seed_projects(data_file, [Project(project_id="P-AAAAAA", title="Alpha")])

    resp = core.update_project_description("P-AAAAAA", "New desc")
    assert resp["success"] is True

    projects, _ = persistence.load_projects(path=data_file)
    assert projects[0].description == "New desc"


#project deadlines
# BLACK-BOX (Equivalent Partitioning): invalid format class (not YYYY-MM-DD) must be rejected.
def test_update_project_deadline_rejects_bad_format(data_file):
    resp = core.update_project_deadline("P-AAAAAA", "2025/01/01")
    assert resp["success"] is False
    assert "yyyy-mm-dd" in resp["message"].lower()


# BLACK-BOX (Equivalent Partitioning): non-existent ID class must return not found for deadline update.
def test_update_project_deadline_not_found(data_file):
    future = (datetime.now().date() + timedelta(days=10)).isoformat()
    resp = core.update_project_deadline("P-NOTREAL", future)
    assert resp["success"] is False
    assert "not found" in resp["message"].lower()

#update project description
# BLACK-BOX (Equivalent Partitioning): invalid status class must be rejected to enforce allowed set.
def test_update_project_status_rejects_invalid_status(data_file):
    resp = core.update_project_status("P-AAAAAA", "INVALID")
    assert resp["success"] is False
    assert "must be one of" in resp["message"].lower()

# BLACK-BOX (Equivalent Partitioning): non-existent ID class must return not found for status update.
def test_update_project_status_not_found(data_file):
    resp = core.update_project_status("P-NOTREAL", "Active")
    assert resp["success"] is False
    assert "not found" in resp["message"].lower()

# update project team and their members
# BLACK-BOX (Equivalent Partitioning): invalid ID class must return not found for team update.
def test_update_project_team_members_not_found(data_file):
    resp = core.update_project_team_members("P-NOTREAL", ["A", "B"])
    assert resp["success"] is False
    assert "not found" in resp["message"].lower()

# BLACK-BOX (Equivalent Partitioning): valid team-members update class should persist members list.
def test_update_project_team_members_success(data_file):
    _seed_projects(data_file, [Project(project_id="P-AAAAAA", title="Alpha")])

    resp = core.update_project_team_members("P-AAAAAA", ["A", "B"])
    assert resp["success"] is True

    projects, _ = persistence.load_projects(path=data_file)
    assert projects[0].team_members == ["A", "B"]

