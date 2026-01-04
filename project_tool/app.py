from __future__ import annotations

from typing import List

from project_tool.core import (
    create_project,
    update_project_title,
    update_project_description,
    update_project_deadline,
    update_project_status,
    update_project_team_members,
    get_active_projects,
    filter_projects_by_status,
)
from project_tool.deletion import list_project_ids, delete_project_by_id
from project_tool.persistence import load_projects

def _print_header(title: str) -> None:
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def _print_response(resp) -> None:
    # our responses are dicts like {"success": bool, "message": "...", "data": ...}
    if isinstance(resp, dict):
        print(resp.get("message", ""))
        if resp.get("data") is not None:
            print(resp["data"])
    else:
        print(resp)


from typing import Optional

def _prompt(text: str, allow_back: bool = False) -> Optional[str]:
    value = input(text).strip()
    if allow_back and value.lower() in ("b", "back"):
        return None
    return value



def _prompt_list(text: str, allow_back: bool = False) -> List[str] | None:
    raw = input(text).strip()
    if allow_back and raw.lower() in ("b", "back"):
        return None
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]

# Menu actions

def _action_create_project() -> None:
    _print_header("Create Project")

    title = _prompt("Project title (B to go back): ", allow_back=True)
    if title is None:
        return

    desc = _prompt("Description (optional) (B to go back): ", allow_back=True)
    if desc is None:
        return

    resp = create_project(title, desc)
    _print_response(resp)



def _action_view_all_projects() -> None:
    _print_header("All Projects")
    projects, msg = load_projects()
    if msg:
        print(msg)

    if not projects:
        print("No projects found.")
        return

    for p in projects:
        print(f"- {p.project_id} | {p.title} | {p.status} | deadline={p.deadline}")


def _action_view_active_projects() -> None:
    _print_header("Active Projects")
    active = get_active_projects()
    if not active:
        print("No active projects.")
        return

    for p in active:
        print(f"- {p.project_id} | {p.title} | deadline={p.deadline}")


def _action_filter_by_status() -> None:
    _print_header("Filter Projects by Status")
    status = _prompt("Enter status (Planning/Active/On Hold/Completed/Archived) (B to go back): ", allow_back=True)
    if status is None:
        return

    filtered = filter_projects_by_status(status)
    if not filtered:
        print(f"No projects found with status '{status}'.")
        return

    for p in filtered:
        print(f"- {p.project_id} | {p.title} | deadline={p.deadline}")


def _action_update_project() -> None:
    _print_header("Update Project")

    pid = _prompt("Project ID (e.g., P-ABC123) (B to go back): ", allow_back=True)
    if pid is None:
        return

    while True:
        print("\nWhat do you want to update?")
        print("1) Title")
        print("2) Description")
        print("3) Deadline")
        print("4) Status")
        print("5) Team members")
        print("B) Back")

        choice = _prompt("Choose 1-5 (or B): ", allow_back=True)
        if choice is None:
            return

        choice = choice.strip()

        if choice == "1":
            new_title = _prompt("New title (B to go back): ", allow_back=True)
            if new_title is None:
                continue
            _print_response(update_project_title(pid, new_title))

        elif choice == "2":
            desc = _prompt("New description (B to go back): ", allow_back=True)
            if desc is None:
                continue
            _print_response(update_project_description(pid, desc))

        elif choice == "3":
            deadline = _prompt("New deadline (YYYY-MM-DD) (B to go back): ", allow_back=True)
            if deadline is None:
                continue
            _print_response(update_project_deadline(pid, deadline))

        elif choice == "4":
            status = _prompt("New status (Planning/Active/On Hold/Completed/Archived) (B to go back): ", allow_back=True)
            if status is None:
                continue
            _print_response(update_project_status(pid, status))

        elif choice == "5":
            members = _prompt_list("Team members (comma-separated) (B to go back): ", allow_back=True)
            if members is None:
                continue
            _print_response(update_project_team_members(pid, members))

        else:
            print("Invalid choice.")
            continue

        again = _prompt("\nUpdate something else for this project? (Y/N): ")
        if again.strip().lower() not in ("y", "yes"):
            return



def _action_delete_project() -> None:
    _print_header("Delete Project")

    ids = list_project_ids()
    if not ids:
        print("No projects to delete.")
        return

    print("Existing project IDs:")
    for pid in ids:
        print(f"- {pid}")

    pid = _prompt("Enter project ID to delete (B to go back): ", allow_back=True)
    if pid is None:
        return

    confirm = _prompt("Confirm deletion (Y/N, B to go back): ", allow_back=True)
    if confirm is None:
        return
    confirm = confirm.strip().lower()

    resp = delete_project_by_id(
        pid,
        confirm=(confirm in ("y", "yes"))
    )

    _print_response(resp)


# Main menu

def main() -> None:
    while True:
        _print_header("Project Management Tool")

        print("1) Create project")
        print("2) View all projects")
        print("3) View active projects")
        print("4) Filter projects by status")
        print("5) Update project")
        print("6) Delete project")
        print("7) Help/About")
        print("8) Exit")

        choice = _prompt("Choose an option (1-7): ")

        if choice == "1":
            _action_create_project()
            input("\nPress Enter to return to the menu...")
        elif choice == "2":
            _action_view_all_projects()
            input("\nPress Enter to return to the menu...")
        elif choice == "3":
            _action_view_active_projects()
            input("\nPress Enter to return to the menu...")
        elif choice == "4":
            _action_filter_by_status()
            input("\nPress Enter to return to the menu...")
        elif choice == "5":
            _action_update_project()
            input("\nPress Enter to return to the menu...")
        elif choice == "6":
            _action_delete_project()
            input("\nPress Enter to return to the menu...")
        elif choice == "7":
            _print_header("About This Tool")
            print("Project Management Tool")
            print("Coursework: Software & Quality Assurance")
            print("Interface: Command Line Interface (CLI)")
            print("Team:Ayobami, Bernard, Daniel, Mody")
            print("\nThis tool supports creating, updating, filtering and deleting projects.")
            input("\nPress Enter to return to the menu...")
        elif choice == "8":
            print("Goodbye.")
            break



        else:
            print("Invalid option.")
            input("\nPress Enter to continue...")
