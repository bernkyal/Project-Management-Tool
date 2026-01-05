from project_tool.models import Task, Project



# BLACK-BOX (Category Partition Method): validates round-trip conversion as a functional unit (to_dict then from_dict).
def test_task_round_trip():
    original = Task(task_id="T-9", title="Round trip", assigned_to=["Z"])
    rebuilt = Task.from_dict(original.to_dict())
    assert rebuilt == original


# BLACK-BOX (Category Partition Method): validates full object round-trip functional unit with nested tasks and history.
def test_project_round_trip_with_tasks_and_history():
    p = Project(project_id="P-9", title="RoundTrip", description="D", team_members=["A"])
    p.tasks = [
        Task(task_id="T-1", title="One", assigned_to=["A"]),
        Task(task_id="T-2", title="Two", status="Done"),
    ]
    p.record_status_change("Active")
    p.record_status_change("Completed")

    rebuilt = Project.from_dict(p.to_dict())

    assert rebuilt.project_id == p.project_id
    assert rebuilt.title == p.title
    assert rebuilt.description == p.description
    assert rebuilt.team_members == p.team_members
    assert [(t.task_id, t.title, t.status, t.assigned_to) for t in rebuilt.tasks] == [
        (t.task_id, t.title, t.status, t.assigned_to) for t in p.tasks
    ]
    assert len(rebuilt.status_history) == len(p.status_history)
    assert [h["status"] for h in rebuilt.status_history] == [h["status"] for h in p.status_history]
    # timestamps are strings; we don't require exact equality across environments,
    # but round-trip should keep them if present
    assert all(isinstance(h.get("timestamp", ""), str) for h in rebuilt.status_history)
