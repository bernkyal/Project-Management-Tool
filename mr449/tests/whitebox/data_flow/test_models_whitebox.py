from project_tool.models import Task, Project

# tasks
# WHITE-BOX (Data Flow Testing): checks definition→use of assigned_to list and ensures copied value prevents aliasing bugs.
def test_task_to_dict_includes_expected_fields_and_copies_lists():
    t = Task(
        task_id="T-1",
        title="Do thing",
        description="desc",
        status="In Progress",
        assigned_to=["A", "B"],
    )

    d = t.to_dict()

    assert d["task_id"] == "T-1"
    assert d["title"] == "Do thing"
    assert d["description"] == "desc"
    assert d["status"] == "In Progress"
    assert d["assigned_to"] == ["A", "B"]

    # should be a copy, not the same
    assert d["assigned_to"] is not t.assigned_to


# WHITE-BOX (Data Flow Testing): tracks data journey of tasks/history definitions into dict uses (serialization correctness).
def test_project_to_dict_includes_tasks_and_history():
    p = Project(project_id="P-1", title="Alpha")
    p.tasks.append(Task(task_id="T-1", title="Task A"))
    p.record_status_change("Active")

    d = p.to_dict()

    assert d["project_id"] == "P-1"
    assert d["title"] == "Alpha"
    assert d["status"] == "Active"
    assert isinstance(d["tasks"], list)
    assert d["tasks"][0]["task_id"] == "T-1"
    assert isinstance(d["status_history"], list)
    assert d["status_history"][0]["status"] == "Active"

