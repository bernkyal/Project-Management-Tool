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


# WHITE-BOX (Statement Testing): executes the strip() statement and confirms whitespace normalization behaviour.
def test_prompt_strips_whitespace(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _prompt: "   hello   ")
    assert app._prompt("x") == "hello"


