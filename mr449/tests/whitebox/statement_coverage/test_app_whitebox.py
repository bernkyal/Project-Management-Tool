import builtins
import project_tool.app as app
from project_tool.models import Project

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

#project tests
# WHITE-BOX (Statement Testing): verifies internal statements update status and append history entry.
def test_project_record_status_change_updates_status_and_appends_history():
    p = Project(project_id="P-1", title="Alpha")

    assert p.status == "Planning"
    assert p.status_history == []

    p.record_status_change("Active")

    assert p.status == "Active"
    assert len(p.status_history) == 1
    entry = p.status_history[0]
    assert entry["status"] == "Active"
    assert "timestamp" in entry
    assert isinstance(entry["timestamp"], str)

    assert len(entry["timestamp"]) > 0  # non-empty string
