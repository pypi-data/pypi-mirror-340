from test2va.bridge import (
    get_capability_options,
    find_profile,
    find_capability,
    check_capability_type,
    save_profile,
)
from test2va.commands import check_prof_path


def capability_add(prof_name, cap, value):
    """Adds a capability to a profile.

    Args:
        prof_name (str): Name of the profile.
        cap (str): Capability name.
        value: Value of the capability.

    Returns:
        None

    Raises:
        None
    """
    check_prof_path()
    prof = find_profile(prof_name)

    if prof is None:
        print(f"Profile '{prof_name}' not found. Create the profile using 'test2va profile create {prof_name}'.")
        return

    cap = find_capability(cap)
    if cap is None:
        print(f"Capability '{cap}' not found. List all capabilities using 'test2va cap list'.")
        return

    correct_type = check_capability_type(cap[0], value)
    if not correct_type:
        print(f"Capability '{cap[0]}' requires a value of type '{cap[1]}'.")
        return

    prof["caps"][cap[0]] = value
    save_profile(prof["name"], prof["apk"], prof["caps"], prof["udid"], prof["api"], prof["java_path"])

    print(f"Capability '{cap[0]}' added to profile '{prof_name}'.")


def capability_docs(cap):
    """Displays documentation for a given capability.

    Args:
        cap (str): Capability name.

    Returns:
        None

    Raises:
        None
    """
    cap = find_capability(cap)
    if cap is None:
        print(f"Capability '{cap}' not found. List all capabilities using 'test2va cap list'.")
        return

    print(f"Capability '{cap[0]}':")
    print(f"Type: {cap[1]}")
    print(f"Description: {cap[2]}")


def capability_edit(prof_name, cap, value):
    """Edits an existing capability in a profile.

    Args:
        prof_name (str): Name of the profile.
        cap (str): Capability name.
        value: New value for the capability.

    Returns:
        None

    Raises:
        None
    """
    check_prof_path()
    prof = find_profile(prof_name)

    if prof is None:
        print(f"Profile '{prof_name}' not found. Create the profile using 'test2va profile create {prof_name}'.")
        return

    cap = find_capability(cap)
    if cap is None:
        print(f"Capability '{cap}' not found. List all capabilities using 'test2va cap list'.")
        return

    correct_type = check_capability_type(cap[0], value)
    if not correct_type:
        print(f"Capability '{cap[0]}' requires a value of type '{cap[1]}'.")
        return

    prof["caps"][cap[0]] = value
    save_profile(prof["name"], prof["apk"], prof["caps"], prof["udid"], prof["api"], prof["java_path"])

    print(f"Capability '{cap[0]}' edited in profile '{prof_name}'.")


def capability_list():
    """Lists all available capabilities and their types.

    Displays them in a two-column format and pauses after every 20 entries.

    Returns:
        None

    Raises:
        None
    """
    caps = get_capability_options()

    for i, cap in enumerate(caps):
        print(f"{cap[0]:<30} {cap[1]}")
        if i % 20 == 19:
            input("Press Enter to continue...")


def capability_remove(prof_name, cap):
    """Removes a capability from a profile.

    Args:
        prof_name (str): Name of the profile.
        cap (str): Capability name.

    Returns:
        None

    Raises:
        None
    """
    check_prof_path()
    prof = find_profile(prof_name)

    if prof is None:
        print(f"Profile '{prof_name}' not found. Create the profile using 'test2va profile create {prof_name}'.")
        return

    cap = find_capability(cap)
    if cap is None:
        print(f"Capability '{cap}' not found. List all capabilities using 'test2va cap list'.")
        return

    if cap[0] in prof["caps"]:
        del prof["caps"][cap[0]]
        save_profile(prof["name"], prof["apk"], prof["caps"], prof["udid"], prof["api"], prof["java_path"])
        print(f"Capability '{cap[0]}' removed from profile '{prof_name}'.")
    else:
        print(f"Profile '{prof_name}' does not have capability '{cap[0]}'.")
