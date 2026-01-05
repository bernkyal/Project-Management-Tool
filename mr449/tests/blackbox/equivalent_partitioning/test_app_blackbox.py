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

# BLACK-BOX (Equivalent Partitioning): input partition {empty string} should map to output partition {empty list}.
def test_prompt_list_empty_returns_empty_list(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _prompt: "")
    assert app._prompt_list("x") == []

# BLACK-BOX (Equivalent Partitioning): valid title/description class should create successfully and print expected confirmation.
def test_action_create_project_happy_path(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["My Title", "My Desc"]))

    monkeypatch.setattr(app, "create_project", lambda title, desc: {
        "success": True,
        "message": f"Created {title} / {desc}"
    })

    app._action_create_project()
    out = capsys.readouterr().out
    assert "Create Project" in out
    assert "Created My Title / My Desc" in out

# BLACK-BOX (Equivalent Partitioning): empty active-set partition should display "No active projects."
def test_action_view_active_projects_no_active(monkeypatch, capsys):
    monkeypatch.setattr(app, "get_active_projects", lambda: [])

    app._action_view_active_projects()
    out = capsys.readouterr().out
    assert "Active Projects" in out
    assert "No active projects." in out

# BLACK-BOX (Equivalent Partitioning): active projects partition should print each active project entry.
def test_action_view_active_projects_prints_active(monkeypatch, capsys):
    monkeypatch.setattr(app, "get_active_projects", lambda: [
        DummyProject("P-1", "A", "Active", None),
        DummyProject("P-2", "B", "Active", "2030-01-01"),
    ])

    app._action_view_active_projects()
    out = capsys.readouterr().out
    assert "Active Projects" in out
    assert "P-1" in out and "A" in out
    assert "P-2" in out and "B" in out

# main menus
# BLACK-BOX (Equivalent Partitioning): partition {user selects exit option} should terminate with "Goodbye."
def test_main_exit_immediately(monkeypatch, capsys):
    # Choose 8 then exit
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["8"]))
    app.main()
    out = capsys.readouterr().out
    assert "Goodbye." in out
