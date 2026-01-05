from project_tool.models import Task, Project

# tasks
# BLACK-BOX (Equivalent Partitioning): partition {missing optional fields} should produce default values consistently.
def test_task_from_dict_defaults_missing_fields():
    t = Task.from_dict({"task_id": 123, "title": "X"})
    assert t.task_id == "123"          # coerced to str
    assert t.title == "X"
    assert t.description == ""
    assert t.status == "Todo"
    assert t.assigned_to == []


# BLACK-BOX (Equivalent Partitioning): partition {missing optional JSON fields} must yield safe defaults.
def test_project_from_dict_handles_missing_optional_fields():
    p = Project.from_dict({"project_id": "P-2", "title": "Beta"})

    assert p.project_id == "P-2"
    assert p.title == "Beta"
    assert p.description == ""
    assert p.deadline is None
    assert p.status == "Planning"
    assert p.team_members == []
    assert p.tasks == []
    assert p.status_history == []

# BLACK-BOX (Equivalent Partitioning): partition {tasks=None} should be normalized to empty list.
def test_project_from_dict_handles_none_tasks():
    p = Project.from_dict(
        {
            "project_id": "P-3",
            "title": "Gamma",
            "tasks": None,
        }
    )
    assert p.tasks == []

