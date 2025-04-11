import json
import os


def read_file_to_string(file_path: str):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"


# def list_to_str(lst: list) -> str:
#     """
#         Appends a list of strings into a single string, handling edge cases like empty strings.
#
#         Args:
#             :param lst: (list of str): A list of strings to append together.
#
#         Returns:
#             str: A single string made by appending all non-empty strings from the list.
#         """
#     if not lst:
#         return ""  # Return empty string if the list is empty
#
#     # Filter out empty strings and join the remaining strings with no separator
#     return ''.join([s for s in lst if s.strip() != ''])


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


def save_json_to_file(data, filepath):
    """
    Saves a dictionary as a JSON file, creating directories if necessary.
    This method will overwrite the file if it already exists.

    Args:
        data (dict): The dictionary to save as JSON.
        filepath (str): The path of the file to save the JSON data to.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Save the JSON data to the file without double encoding
    with open(filepath, 'w') as file:
        # Use json.dump() directly to avoid double encoding
        json.dump(data, file, indent=4)

    print(f"Data successfully saved to {filepath}")


def get_java_test_method_names(directory) -> list[str]:
    """
    Returns a list of all Java file names (without the .java extension),
    with the first letter in lowercase, from the given directory.

    Args:
        directory (str): The path to the directory to search for Java files.

    Returns:
        list: A list of Java file names without the .java extension, with the first letter in lowercase.
    """
    java_files_names = []

    for filename in os.listdir(directory):
        if filename.endswith('.java'):
            # Remove the .java extension and convert the first character to lowercase
            base_name = filename[:-5]
            base_name_lowercase = base_name[0].lower() + base_name[1:]
            java_files_names.append(base_name_lowercase)

    return java_files_names


def get_java_test_file_names(directory) -> list[str]:
    """
    Returns a list of all Java file names (without the .java extension),
    with the first letter in lowercase, from the given directory.

    Args:
        directory (str): The path to the directory to search for Java files.

    Returns:
        list: A list of Java file names without the .java extension, with the first letter in lowercase.
    """
    java_files_names = []

    for filename in os.listdir(directory):
        if filename.endswith('.java'):
            # Remove the .java extension and convert the first character to lowercase
            base_name = filename[:-5]
            base_name_lowercase = base_name[0] + base_name[1:]
            java_files_names.append(base_name_lowercase)

    return java_files_names

