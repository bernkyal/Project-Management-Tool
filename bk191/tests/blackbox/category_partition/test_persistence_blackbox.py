import json
from project_tool.models import Project
from project_tool.persistence import (
    ensure_data_file_exists,
    validate_before_save,
    load_projects,
    save_projects,
)

# Helper files

def _make_project(pid="P-AAA111", title="Title", status="Planning") -> Project:
    return Project(project_id=pid, title=title, status=status)


# test saving all the projects
# BLACK-BOX (Category Partition Method): category "pre-save validation" with choice {fail} should block file write.
def test_save_projects_fails_if_validation_fails(tmp_path):
    test_file = tmp_path / "projects.json"
    bad = [_make_project(pid="", title="A")]

    ok, msg = save_projects(bad, path=str(test_file))
    assert ok is False
    assert "missing a project_id" in msg.lower()

 # BLACK-BOX (Category Partition Method): validates full save functional unit producing correct JSON list output.
def test_save_projects_writes_projects(tmp_path):
    test_file = tmp_path / "projects.json"
    projects = [_make_project(pid="P-1", title="Alpha"), _make_project(pid="P-2", title="Beta")]

    ok, msg = save_projects(projects, path=str(test_file))
    assert ok is True
    assert msg in ("", None)

    raw = json.loads(test_file.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    assert {p["project_id"] for p in raw} == {"P-1", "P-2"}

# BLACK-BOX (Category Partition): category {list contains invalid project dict} should skip/return error safely.
def test_load_projects_handles_project_missing_required_fields(tmp_path):
    test_file = tmp_path / "projects.json"
    payload = [{"title": "A"}]  # missing project_id, etc.
    test_file.write_text(json.dumps(payload), encoding="utf-8")

    projects, msg = load_projects(path=str(test_file))
    # Your code might skip invalid rows or fail the whole load.
    # Either way, it must not crash.
    assert isinstance(projects, list)
    assert msg is None or isinstance(msg, str)


# BLACK-BOX (Category Partition): JSONDecodeError is handled, file is reset to [].
def test_load_projects_corrupted_json_resets_file(tmp_path):
    p = tmp_path / "projects.json"
    p.write_text("{", encoding="utf-8")  # invalid JSON

    projects, msg = load_projects(path=str(p))
    assert projects == []
    assert "corrupted" in msg.lower()
    assert json.loads(p.read_text(encoding="utf-8")) == []

# BLACK-BOX (Category Partition): save_projects writes project data successfully.
def test_save_projects_happy_path(tmp_path):
    p = tmp_path / "projects.json"
    projects = [Project(project_id="P-1", title="Alpha", status="Planning")]

    ok, msg = save_projects(projects, path=str(p))
    assert ok is True
    assert msg == ""
    assert {x["project_id"] for x in json.loads(p.read_text(encoding="utf-8"))} == {"P-1"}

# BLACK-BOX (Category Partition): ensure_data_file_exists creates the folder and initialises file with [].
def test_ensure_data_file_exists_creates_parent_and_file(tmp_path):
    import json

    p = tmp_path / "data" / "projects.json"  # folder doesn't exist initially
    ensure_data_file_exists(path=str(p))

    assert p.exists()
    assert json.loads(p.read_text(encoding="utf-8")) == []

def test_save_projects_success_path_covers_temp_write_and_replace(tmp_path):

    p = tmp_path / "projects.json"
    projects = [Project(project_id="P-1", title="Alpha", status="Planning")]

    ok, msg = save_projects(projects, path=str(p))
    assert ok is True
    assert msg == ""

    raw = json.loads(p.read_text(encoding="utf-8"))
    assert raw[0]["project_id"] == "P-1"
