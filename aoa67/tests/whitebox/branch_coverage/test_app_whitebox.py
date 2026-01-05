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

# WHITE-BOX (Branch Testing): hits back/exit branch in status filtering action (user chooses 'B').
def test_action_filter_by_status_back(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "B")

    app._action_filter_by_status()
    out = capsys.readouterr().out
    assert "Filter Projects by Status" in out

# WHITE-BOX (Branch Testing): forces early exit branch when PID prompt receives back token.
def test_action_update_project_back_on_pid(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _prompt="": "B")
    app._action_update_project()
    out = capsys.readouterr().out
    assert "Update Project" in out

# WHITE-BOX (Loop Testing): drives the update menu loop through invalid choice path then exits via back.
def test_action_update_project_invalid_choice_then_back(monkeypatch, capsys):
    # pid, invalid choice, then B to exit
    monkeypatch.setattr(builtins, "input", _make_input_feeder(["P-AAAAAA", "9", "B"]))

    app._action_update_project()
    out = capsys.readouterr().out
    assert "Update Project" in out
    assert "Invalid choice." in out

# WHITE-BOX (Branch Testing): chooses menu option 1 and executes the internal title-update path.
def test_action_update_project_title_path(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _make_input_feeder([
        "P-AAAAAA",  # pid
        "1",         # choose Title
        "New Title", # new title
        "n"          # stop updating
    ]))

    monkeypatch.setattr(app, "update_project_title", lambda pid, title: {
        "success": True,
        "message": f"{pid} title updated to {title}"
    })

    app._action_update_project()
    out = capsys.readouterr().out
    assert "Update Project" in out
    assert "title updated" in out.lower()

# WHITE-BOX (Branch Testing): chooses menu option 2 and executes the internal description-update path.
def test_action_update_project_description_path(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _make_input_feeder([
        "P-AAAAAA",
        "2",
        "New Desc",
        "no",
    ]))

    monkeypatch.setattr(app, "update_project_description", lambda pid, desc: {
        "success": True,
        "message": f"{pid} desc updated"
    })

    app._action_update_project()
    out = capsys.readouterr().out
    assert "desc updated" in out.lower()

# WHITE-BOX (Branch Testing): chooses menu option 3 and executes the internal deadline-update path.
def test_action_update_project_deadline_path(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _make_input_feeder([
        "P-AAAAAA",
        "3",
        "2030-01-01",
        "n",
    ]))

    monkeypatch.setattr(app, "update_project_deadline", lambda pid, dl: {
        "success": True,
        "message": f"{pid} deadline updated"
    })

    app._action_update_project()
    out = capsys.readouterr().out
    assert "deadline updated" in out.lower()

# WHITE-BOX (Branch Testing): chooses menu option 4 and executes the internal status-update path.
def test_action_update_project_status_path(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _make_input_feeder([
        "P-AAAAAA",
        "4",
        "Active",
        "n",
    ]))

    monkeypatch.setattr(app, "update_project_status", lambda pid, st: {
        "success": True,
        "message": f"{pid} status updated to {st}"
    })

    app._action_update_project()
    out = capsys.readouterr().out
    assert "status updated" in out.lower()
    assert "active" in out.lower()

# WHITE-BOX (Branch Testing): chooses menu option 5 and executes the internal team-members-update path.
def test_action_update_project_team_members_path(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", _make_input_feeder([
        "P-AAAAAA",
        "5",
        "Alice, Bob",
        "n",
    ]))

    monkeypatch.setattr(app, "update_project_team_members", lambda pid, members: {
        "success": True,
        "message": f"{pid} team updated",
        "data": members
    })

    app._action_update_project()
    out = capsys.readouterr().out
    assert "team updated" in out.lower()
    assert "Alice" in out and "Bob" in out
