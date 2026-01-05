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

# Validate before saving the code
# BLACK-BOX (Equivalent Partitioning): invalid data class {missing project_id} must be rejected by validation.
def test_validate_before_save_fails_missing_project_id():
    projects = [_make_project(pid="")]
    ok, msg = validate_before_save(projects)
    assert ok is False
    assert "missing a project_id" in msg

# BLACK-BOX (Equivalent Partitioning): invalid data class {empty title} must be rejected by validation.
def test_validate_before_save_fails_empty_title():
    projects = [_make_project(title="   ")]
    ok, msg = validate_before_save(projects)
    assert ok is False
    assert "empty title" in msg

# BLACK-BOX (Equivalent Partitioning): invalid data class {duplicate IDs} must be rejected to prevent collisions.
def test_validate_before_save_fails_duplicate_project_id():
    projects = [_make_project(pid="P-1", title="A"), _make_project(pid="P-1", title="B")]
    ok, msg = validate_before_save(projects)
    assert ok is False
    assert "Duplicate project_id" in msg

# BLACK-BOX (Equivalent Partitioning): valid data class should pass validation.
def test_validate_before_save_ok():
    projects = [_make_project(pid="P-1", title="A"), _make_project(pid="P-2", title="B")]
    ok, msg = validate_before_save(projects)
    assert ok is True
    assert msg == ""


# load all of our testing projects
# BLACK-BOX (Equivalent Partitioning): partition {storage file missing} should return empty list and not crash.
def test_load_projects_returns_empty_when_file_missing(tmp_path):
    test_file = tmp_path / "projects.json"
    projects, msg = load_projects(path=str(test_file))
    assert projects == []
    assert msg in ("", None)  # ensure created, no error

# BLACK-BOX (Equivalent Partitioning): valid JSON list partition should parse into Project objects correctly
def test_load_projects_parses_projects(tmp_path):
    test_file = tmp_path / "projects.json"
    payload = [
        {"project_id": "P-1", "title": "A", "status": "Planning", "description": "", "deadline": None,
         "team_members": [], "tasks": [], "status_history": []}
    ]
    test_file.write_text(json.dumps(payload), encoding="utf-8")

    projects, msg = load_projects(path=str(test_file))
    assert msg in ("", None)
    assert len(projects) == 1
    assert projects[0].project_id == "P-1"
    assert projects[0].title == "A"


# BLACK-BOX (Equivalent Partitioning): invalid JSON partition must not crash; should return [] + error message (or safe msg).
def test_load_projects_handles_invalid_json(tmp_path):
    test_file = tmp_path / "projects.json"
    test_file.write_text("{", encoding="utf-8")  # invalid JSON

    projects, msg = load_projects(path=str(test_file))
    assert projects == []
    # Depending on your implementation, msg may be "", None, or an error string.
    # If your code sets an error message, this makes it count as "expected/actual" documented behavior.
    assert msg is None or isinstance(msg, str)

# BLACK-BOX (Equivalent Partitioning): invalid data class {JSON is not a list} must be rejected safely.
def test_load_projects_rejects_non_list_json(tmp_path):
    test_file = tmp_path / "projects.json"
    test_file.write_text(json.dumps({"project_id": "P-1"}), encoding="utf-8")  # dict not list

    projects, msg = load_projects(path=str(test_file))
    assert projects == []
    assert msg is None or isinstance(msg, str)

# BLACK-BOX (Equivalence Partitioning): invalid partition {top-level not a list} -> returns [] with invalid format message.
def test_load_projects_rejects_non_list_format(tmp_path):
    path = tmp_path / "projects.json"
    path.write_text(json.dumps({"x": 1}), encoding="utf-8")  # dict instead of list

    projects, msg = load_projects(path=str(path))
    assert projects == []
    assert "format is invalid" in msg.lower()

# BLACK-BOX (Equivalence Partitioning): partition {raw None} -> returns [] with 'was empty' message.
def test_load_projects_raw_none_returns_empty_with_message(tmp_path):
    path = tmp_path / "projects.json"
    path.write_text("null", encoding="utf-8")  # json.load => None

    projects, msg = load_projects(path=str(path))
    assert projects == []
    assert "was empty" in msg.lower()

# BLACK-BOX (Equivalence Partitioning): load_projects returns empty list with "was empty" message.
def test_load_projects_raw_none(tmp_path):

    p = tmp_path / "projects.json"
    p.write_text("null", encoding="utf-8")

    projects, msg = load_projects(path=str(p))
    assert projects == []
    assert "was empty" in msg.lower()

# BLACK-BOX (Equivalence Partitioning): load_projects rejects format and returns empty list.
def test_load_projects_non_list(tmp_path):

    p = tmp_path / "projects.json"
    p.write_text(json.dumps({"a": 1}), encoding="utf-8")

    projects, msg = load_projects(path=str(p))
    assert projects == []
    assert "expected a list" in msg.lower()

# BLACK-BOX (Equivalence Partitioning): load_projects parses into Project objects.
def test_load_projects_valid_list_parses(tmp_path):
    p = tmp_path / "projects.json"
    payload = [{
        "project_id": "P-1",
        "title": "A",
        "status": "Planning",
        "description": "",
        "deadline": None,
        "team_members": [],
        "tasks": [],
        "status_history": [],
    }]
    p.write_text(json.dumps(payload), encoding="utf-8")

    projects, msg = load_projects(path=str(p))
    assert msg == ""
    assert len(projects) == 1
    assert projects[0].project_id == "P-1"
