from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    task_id: str
    title: str
    description: str = ""
    status: str = "Todo"  # Todo / In Progress / Done
    assigned_to: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "assigned_to": list(self.assigned_to),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        return Task(
            task_id=str(data.get("task_id", "")),
            title=str(data.get("title", "")),
            description=str(data.get("description", "")),
            status=str(data.get("status", "Todo")),
            assigned_to=list(data.get("assigned_to", [])),
        )


@dataclass
class Project:
    project_id: str
    title: str
    description: str = ""
    deadline: Optional[str] = None  # "YYYY-MM-DD"
    status: str = "Planning"  # Planning / Active / On Hold / Completed / Archived
    team_members: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    # M8: record when status changes
    status_history: List[Dict[str, str]] = field(default_factory=list)

    def record_status_change(self, new_status: str) -> None:
        self.status = new_status
        self.status_history.append(
            {"status": new_status, "timestamp": datetime.now().isoformat(timespec="seconds")}
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "status": self.status,
            "team_members": list(self.team_members),
            "tasks": [t.to_dict() for t in self.tasks],
            "status_history": list(self.status_history),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Project":
        tasks_data = data.get("tasks", []) or []
        tasks = [Task.from_dict(t) for t in tasks_data]

        return Project(
            project_id=str(data.get("project_id", "")),
            title=str(data.get("title", "")),
            description=str(data.get("description", "")),
            deadline=data.get("deadline", None),
            status=str(data.get("status", "Planning")),
            team_members=list(data.get("team_members", [])),
            tasks=tasks,
            status_history=list(data.get("status_history", [])),
        )