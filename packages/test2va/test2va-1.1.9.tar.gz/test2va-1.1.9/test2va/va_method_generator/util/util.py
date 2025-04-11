import json
import os


def read_file_to_string(file_path: str):
    """
    Reads the entire file as a single string.

    :param file_path: Path to the file to be read.
    :return: The contents of the file as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()  # Read the entire file as a single string
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""


def list_to_str(strings: list[str]) -> str:
    """
    Appends a list of strings into a single string
    :param strings: input string list
    :return: A single string made by appending all non-empty strings from the list.
    """
    # Use a list comprehension to filter out empty strings
    filtered_strings = [s for s in strings if s]

    # Join the non-empty strings with a newline character
    result = "\n".join(filtered_strings)

    # Add a newline at the end, if the result is not empty
    if result:
        result += "\n"
    return result

