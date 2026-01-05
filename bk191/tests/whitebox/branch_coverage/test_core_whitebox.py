import re
from datetime import datetime, timedelta
import pytest
import project_tool.core as core
import project_tool.persistence as persistence
from project_tool.models import Project
import json
import os

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

def _make_project(pid="P-AAA111", title="Title", status="Planning") -> Project:
    return Project(project_id=pid, title=title, status=status)

# WHITE-BOX (Branch Testing): forces internal save-failure branch to confirm correct error handling path.
def test_create_project_returns_error_if_save_fails(data_file, monkeypatch):
    def fake_save(_projects):
        return False, "disk error"

    monkeypatch.setattr(core, "save_projects", fake_save)

    resp = core.create_project("X", "Y")
    assert resp["success"] is False
    assert "disk error" in resp["message"].lower()

# WHITE-BOX (Branch Coverage): execute save happy path (covers 103-104 and success path within 113-125).
def test_save_projects_happy_path_executes_temp_write_and_replace(tmp_path):
    p = tmp_path / "projects.json"
    projects = [_make_project("P-1", "Alpha"), _make_project("P-2", "Beta")]

    ok, msg = persistence.save_projects(projects, path=str(p))

    assert ok is True
    assert msg == ""

    # confirm file contains expected IDs
    raw = json.loads(p.read_text(encoding="utf-8"))
    assert {x["project_id"] for x in raw} == {"P-1", "P-2"}

    # bonus: ensure temp file is not left behind (often indicates replace ran)
    assert not (tmp_path / "projects.json.tmp").exists()


# WHITE-BOX (Branch Coverage): force os.replace to raise -> execute OSError branch (covers exception part of 113-125).
def test_save_projects_oserror_branch_on_replace(tmp_path, monkeypatch):
    p = tmp_path / "projects.json"
    projects = [_make_project("P-1", "Alpha")]

    def failing_replace(src, dst):
        raise OSError("boom")

    monkeypatch.setattr(os, "replace", failing_replace)

    ok, msg = persistence.save_projects(projects, path=str(p))
    assert ok is False
    assert "could not save projects file" in msg.lower()


# WHITE-BOX (Branch Coverage): stop_autosave sets stop event (covers line 130).
def test_stop_autosave_sets_event():
    persistence._autosave_stop_event.clear()
    assert persistence._autosave_stop_event.is_set() is False

    persistence.stop_autosave()
    assert persistence._autosave_stop_event.is_set() is True