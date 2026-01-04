from typing import Any, Dict

# Response helpers

def success(message: str, data: Any = None) -> Dict[str, Any]:

   # A10, M4, D4, D9:

    response = {
        "success": True,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return response


def error(message: str) -> Dict[str, Any]:

    return {
        "success": False,
        "message": message,
    }




def project_created(project_id: str) -> Dict[str, Any]:

    #M4
    #Confirmation message after creating a project.

    return success(f"Project '{project_id}' created successfully.")


def project_updated(project_id: str, field_name: str) -> Dict[str, Any]:

   # A1–A5, A10:
   # Confirmation after updating a project field.

    return success(f"Project '{project_id}' updated ({field_name}).")


def project_deleted(project_id: str) -> Dict[str, Any]:

   # D4:
   # Confirmation after deleting a project.

    return success(f"Project '{project_id}' deleted successfully.")


def project_not_found(project_id: str) -> Dict[str, Any]:

   # D2, A10:
   # Error when a project does not exist.

    return error(f"Project '{project_id}' was not found.")


def invalid_input(reason: str) -> Dict[str, Any]:

   # A6–A10, D3, D6:
   # Generic invalid input message.

    return error(f"Invalid input: {reason}")