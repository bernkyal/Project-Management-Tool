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


# BLACK-BOX (Equivalent Partitioning): partition {valid status with 0 matches} should yield "No projects found" message.
def test_action_filter_by_status_no_matches(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["Active"]))
    monkeypatch.setattr(app, "filter_projects_by_status", lambda status: [])

    app._action_filter_by_status()
    out = capsys.readouterr().out
    assert "Filter Projects by Status" in out
    assert "No projects found with status 'Active'." in out

# BLACK-BOX (Equivalent Partitioning): partition {valid status with matches} should print matched project(s).
def test_action_filter_by_status_with_matches(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["On Hold"]))
    monkeypatch.setattr(app, "filter_projects_by_status", lambda status: [
        DummyProject("P-9", "HoldMe", status="On Hold", deadline=None)
    ])

    app._action_filter_by_status()
    out = capsys.readouterr().out
    assert "Filter Projects by Status" in out
    assert "P-9" in out and "HoldMe" in out


