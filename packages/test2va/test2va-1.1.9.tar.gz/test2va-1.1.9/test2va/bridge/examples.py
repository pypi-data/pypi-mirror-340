import os


def list_examples() -> tuple:
    """
    Returns a tuple of available example names.

    Returns:
        tuple: A tuple containing the names of available examples.
    """
    return "NOTES_SetLeftSwipeToDelete", "NOTES_CreateLabel"


def get_example_data(ex: str) -> dict or None:
    """
    Retrieves example data based on the provided example name.

    Args:
        ex (str): The name of the example.

    Returns:
        dict or None: A dictionary containing example details (app path, java file path, and activity)
                      if the example exists, otherwise None.
    """
    m = {
        "Select an example": {
            "app": "Enter file path to app apk",
            "java": "Enter file path to java file",
            "activity": "",
        },
        "NOTES_SetLeftSwipeToDelete": {
            "app": os.path.join(os.path.dirname(__file__), "../examples", "NOTES", "another-notes-app.apk"),
            "java": os.path.join(os.path.dirname(__file__), "../examples", "NOTES", "NOTES_SetLeftSwipeToDelete.java"),
            "activity": "com.maltaisn.notes.ui.main.MainActivity",
        },
        "NOTES_CreateLabel": {
            "app": os.path.join(os.path.dirname(__file__), "../examples", "NOTES", "another-notes-app.apk"),
            "java": os.path.join(os.path.dirname(__file__), "../examples", "NOTES", "NOTES_CreateLabel.java"),
            "activity": "com.maltaisn.notes.ui.main.MainActivity",
        },
    }

    return m.get(ex)
