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

# WHITE-BOX (Branch Testing): forces the back/exit branch inside _prompt_list when allow_back=True.
def test_prompt_list_back_returns_none(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _prompt: "B")
    assert app._prompt_list("x", allow_back=True) is None

# WHITE-BOX (Branch Testing): triggers early-return/back branch so create_project is not executed.
def test_action_create_project_back_does_not_call_create(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _prompt: "B")

    called = {"count": 0}

    def fake_create(*args, **kwargs):
        called["count"] += 1
        return {"success": True, "message": "should not happen"}

    monkeypatch.setattr(app, "create_project", fake_create)

    app._action_create_project()
    out = capsys.readouterr().out
    assert "Create Project" in out
    assert called["count"] == 0
