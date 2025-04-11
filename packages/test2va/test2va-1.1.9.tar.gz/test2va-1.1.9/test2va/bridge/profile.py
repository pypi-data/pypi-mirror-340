"""
Module for managing profiles, including saving, deleting, and retrieving profile information.
Profiles are stored in a dedicated directory with a JSON file describing each profile.
The goal of profiles are to reuse testing information to streamline user experience.
"""

import json
import os

prof_path = os.path.join(os.path.dirname(__file__), "../profiles")
max_prof_name_len = 28


def save_profile(name, apk="", caps={}, udid="", api="", j_path="", j_code=None):
    """Save a profile with the provided configuration details.

    The profile information is saved to a JSON file inside a dedicated directory for the profile.
    If Java source code is provided via `j_code`, it will be saved to a file and its path will be recorded.

    Args:
        name (str): Name of the profile. The name will be truncated to a maximum length of 28 characters.
        apk (str, optional): Path to the APK file. Defaults to an empty string.
        caps (dict, optional): Capabilities dictionary for the profile. Defaults to an empty dictionary.
        udid (str, optional): Device UDID. Defaults to an empty string.
        api (str, optional): OpenAI API key associated with the profile. Defaults to an empty string.
        j_path (str, optional): Path to the Java source file. Defaults to an empty string.
        j_code (str, optional): Direct input java source code. If provided, the file is saved and its path is used.
                                Defaults to None.

    Returns:
        str: The directory path where the profile has been saved.
    """
    name = name[:max_prof_name_len]

    if not os.path.exists(os.path.join(prof_path, name)):
        os.makedirs(os.path.join(prof_path, name))

    prof_dir = os.path.join(prof_path, name)

    if j_code is not None:
        with open(os.path.join(prof_dir, "java_src_code.java"), "w") as file:
            file.write(j_code)
        j_path = os.path.join(prof_dir, "java_src_code.java")

    if len(apk) > 0:
        apk = os.path.abspath(apk)

    if len(j_path) > 0:
        j_path = os.path.abspath(j_path)

    data = {
        "apk": apk,
        "caps": caps,
        "java_path": j_path,
        "udid": udid,
        "api": api
    }

    with open(os.path.join(prof_dir, "profile.json"), "w") as file:
        json.dump(data, file)

    return prof_dir


def delete_profile(name):
    """Delete a profile by removing its directory and all contained files.

    Args:
        name (str): Name of the profile to delete.

    Returns:
        bool: True if the profile existed and was successfully deleted, False otherwise.
    """
    prof_dir = os.path.join(prof_path, name)
    if os.path.exists(prof_dir):
        for root, dirs, files in os.walk(prof_dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(prof_dir)
        return True
    return False


def find_profile(name):
    """Find and return a profile by its name.

    This function retrieves all profiles and returns the first profile matching the given name.

    Args:
        name (str): The name of the profile to search for.

    Returns:
        dict or None: A dictionary containing profile data if found; otherwise, None.
    """
    profs = get_profiles()
    for prof in profs:
        if prof["name"] == name:
            return prof
    return None


def get_profiles():
    """Retrieve all stored profiles.

    The function walks through the profiles directory and loads the JSON configuration from each profile's folder.

    Returns:
        list of dict: A list where each element is a dictionary representing a profile with keys:
                      'name', 'apk', 'api', 'caps', 'java_path', and 'udid'.
    """
    profiles = []
    for root, dirs, files in os.walk(prof_path):
        for name in dirs:
            prof = os.path.join(prof_path, name, "profile.json")
            if not os.path.exists(prof):
                continue

            with open(prof, "r") as file:
                data = json.load(file)

            profiles.append({
                "name": name,
                "apk": data["apk"],
                "api": data["api"],
                "caps": data["caps"],
                "java_path": data["java_path"],
                "udid": data["udid"]
            })

    return profiles
