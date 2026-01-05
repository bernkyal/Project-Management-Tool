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

# WHITE-BOX (Branch Testing): triggers back branch during delete workflow after showing available IDs.
def test_action_delete_project_back_on_pid(monkeypatch, capsys):
    monkeypatch.setattr(app, "list_project_ids", lambda: ["P-1"])
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "B")

    app._action_delete_project()
    out = capsys.readouterr().out
    assert "Existing project IDs:" in out
    assert "P-1" in out
