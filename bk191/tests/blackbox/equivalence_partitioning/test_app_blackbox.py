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

# BLACK-BOX (Equivalent Partitioning): non-empty project list partition should display formatted project details.
def test_action_view_all_projects_prints_projects(monkeypatch, capsys):
    dummy = [
        DummyProject("P-AAAAAA", "Alpha", "Planning", None),
        DummyProject("P-BBBBBB", "Beta", "Active", "2030-01-01"),
    ]
    monkeypatch.setattr(app, "load_projects", lambda: (dummy, ""))

    app._action_view_all_projects()
    out = capsys.readouterr().out
    assert "All Projects" in out
    assert "P-AAAAAA" in out and "Alpha" in out
    assert "P-BBBBBB" in out and "Beta" in out

# BLACK-BOX (Equivalent Partitioning): empty projects partition should produce "No projects found" + message output.
def test_action_view_all_projects_handles_message_and_no_projects(monkeypatch, capsys):
    monkeypatch.setattr(app, "load_projects", lambda: ([], "warning"))

    app._action_view_all_projects()
    out = capsys.readouterr().out
    assert "All Projects" in out
    assert "warning" in out
    assert "No projects found." in out

