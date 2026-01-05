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

# main menus
# WHITE-BOX (Loop Testing): exercises the main menu loop through invalid-choice branch, then continues and exits.
def test_main_invalid_option_then_exit(monkeypatch, capsys):
    # invalid option, press enter to continue, then exit
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["999", "", "8"]))
    app.main()
    out = capsys.readouterr().out
    assert "Invalid option." in out
