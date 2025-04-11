import json

from test2va.const import JSON_INDENT

def write_json(data, path):
    """
    Writes data to a JSON file with a specified indentation.

    Args:
        data (Any): The data to be written to the JSON file.
        path (str): The file path where the JSON data should be saved.

    Returns:
        None

    Example:
        >>> data = {"name": "Alice", "age": 25}
        >>> write_json(data, "output.json")
    """
    with open(path, "w") as file:
        json.dump(data, file, indent=JSON_INDENT)


def read_json(path):
    """
    Reads data from a JSON file and returns the parsed JSON object.

    Args:
        path (str): The file path of the JSON file to be read.

    Returns:
        Any: The parsed JSON data.

    Example:
        >>> data = read_json("output.json")
        >>> print(data)
        {'name': 'Alice', 'age': 25}
    """
    with open(path, "r") as file:
        return json.load(file)
