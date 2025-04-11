import os


def check_file_exists(file_path: str, print_func=print) -> bool:
    """
    Checks if a file exists at the given path and prints a message if it does not.

    Args:
        file_path (str): The path of the file to check.
        print_func (callable, optional): A function to use for printing messages. Defaults to `print`.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    exists = os.path.exists(file_path)

    if not exists:
        print_func(f"⛔ File: '{file_path}' does not exist\n")
        return False

    return True
