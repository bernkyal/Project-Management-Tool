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

# BLACK-BOX (Category Partition Method): partitions "list input" into categories (names, spaces, empty entries) and checks valid choices are kept.
def test_prompt_list_splits_and_strips(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _prompt: " Alice,  Bob , , Charlie  ")
    assert app._prompt_list("x") == ["Alice", "Bob", "Charlie"]

# BLACK-BOX (Category Partition Method): category "menu option" with choice "About" must produce About output then allow exit.
def test_main_about_then_exit(monkeypatch, capsys):
    # About, press enter, then exit
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["7", "", "8"]))
    app.main()
    out = capsys.readouterr().out
    assert "About This Tool" in out
    assert "Project Management Tool" in out

# BLACK-BOX (Category Partition Method): partitions menu selection path (Create → Continue → Exit) as a valid functional flow.
def test_main_routes_to_create_then_exit(monkeypatch, capsys):
    # Choose create, then supply title/desc, then press enter, then exit
    monkeypatch.setattr(builtins, "input", _make_input_feeder([
        "1", "Title", "Desc", "", "8"
    ]))

    monkeypatch.setattr(app, "create_project", lambda title, desc: {
        "success": True,
        "message": f"Created {title} / {desc}"
    })

    app.main()
    out = capsys.readouterr().out
    assert "Create Project" in out
    assert "Created Title / Desc" in out
    assert "Goodbye." in out
