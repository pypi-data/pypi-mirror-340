common_permissions = [
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    #"android.permission.WRITE_CONTACTS",
    "android.permission.GET_ACCOUNTS",
    "android.permission.ACCESS_WIFI_STATE",
    "android.permission.CHANGE_WIFI_STATE",
    "android.permission.BLUETOOTH",
    "android.permission.BLUETOOTH_ADMIN",
    "android.permission.READ_PHONE_STATE",
    "android.permission.CALL_PHONE",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
    "android.permission.ADD_VOICEMAIL",
    "android.permission.PROCESS_OUTGOING_CALLS",
    "android.permission.POST_NOTIFICATIONS",
    "android.permission.VIBRATE",
    "android.permission.SCHEDULE_EXACT_ALARM",
    #"android.permission.WRITE_EXTERNAL_STORAGE",
    #"android.permission.READ_EXTERNAL_STORAGE",
    #"android.permission.MANAGE_EXTERNAL_STORAGE",
]


def grant_permissions(driver, app_id, grant_perms=True):
    """Grants required runtime permissions to a specified Android application.

    This function retrieves the currently granted permissions for the app,
    combines them with a predefined list of common permissions, and grants
    them using the Appium `mobile: shell` command.

    Args:
        driver (appium.webdriver.webdriver.WebDriver): The Appium WebDriver instance.
        app_id (str): The package name (application ID) of the app.
        grant_perms (bool, optional): If `False`, the function exits without granting permissions. Defaults to `True`.

    Returns:
        None
    """
    if not grant_perms:
        return

    out = driver.execute_script("mobile: shell", {"command": "dumpsys package " + app_id, "args": []})
    # Find all lines that start with "   Permission "
    permissions = [line for line in out.split("\n") if line.startswith("  Permission ")]
    # Slice "  Permission " off of the beginning of each line
    permissions = [permission[13:] for permission in permissions]
    # Slice it from the beginning bracket to the next closing bracket []
    permissions = [permission[1:permission.index("]")] for permission in permissions]
    # Finally, combine the common permissions with the permissions that the app already has and remove duplicates.
    permissions = list(set(permissions + common_permissions))
    for permission in permissions:
        #print(permission)
        try:
            command = f"pm grant {app_id} {permission}"
            driver.execute_script("mobile: shell", {"command": command})
        except:
            pass
