import builtins
import project_tool.app as app

class DummyProject:
    def __init__(self, project_id, title, status="Planning", deadline=None):
        self.project_id = project_id
        self.title = title
        self.status = status
        self.deadline = deadline

def _make_input_feeder(values):
    it = iter(values)
    return lambda _prompt="": next(it)


# BLACK-BOX (Equivalent Partitioning): partition {no project IDs exist} should result in "No projects to delete."
def test_action_delete_project_no_projects(monkeypatch, capsys):
    monkeypatch.setattr(app, "list_project_ids", lambda: [])

    app._action_delete_project()
    out = capsys.readouterr().out
    assert "Delete Project" in out
    assert "No projects to delete." in out

 # BLACK-BOX (Equivalent Partitioning): partition {confirmation = No} should call delete with confirm=False and show expected message.
def test_action_delete_project_confirm_no(monkeypatch, capsys):
    monkeypatch.setattr(app, "list_project_ids", lambda: ["P-1"])
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["P-1", "n"]))

    # Ensure confirm False is passed
    def fake_delete(pid, confirm):
        assert pid == "P-1"
        assert confirm is False
        return {"success": True, "message": "deleted? nope"}

    monkeypatch.setattr(app, "delete_project_by_id", fake_delete)

    app._action_delete_project()
    out = capsys.readouterr().out
    assert "deleted? nope" in out

# BLACK-BOX (Equivalent Partitioning): partition {confirmation = Yes} should call delete with confirm=True and show success message.
def test_action_delete_project_confirm_yes(monkeypatch, capsys):
    monkeypatch.setattr(app, "list_project_ids", lambda: ["P-1"])
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["P-1", "Y"]))

    def fake_delete(pid, confirm):
        assert confirm is True
        return {"success": True, "message": f"{pid} deleted successfully"}

    monkeypatch.setattr(app, "delete_project_by_id", fake_delete)

    app._action_delete_project()
    out = capsys.readouterr().out
    assert "deleted successfully" in out.lower()

