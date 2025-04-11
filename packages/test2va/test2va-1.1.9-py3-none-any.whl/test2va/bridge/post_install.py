import os

# Define paths for example assets and profiles
ex_asset_path = os.path.join(os.path.dirname(__file__), "../examples", "NOTES")
apk_path = os.path.abspath(os.path.join(ex_asset_path, "another-notes-app.apk"))
cl_path = os.path.abspath(os.path.join(ex_asset_path, "CreateLabelTest.java"))
sls_path = os.path.abspath(os.path.join(ex_asset_path, "SetLeftSwipeToDelete.java"))

profile_path = os.path.join(os.path.dirname(__file__), "../profiles")

# Define JSON strings for different test scenarios
create_label = '{"apk": ' + f'"{apk_path}"' + ', "caps": {"app_wait_activity": ' \
                                              '"com.maltaisn.notes.ui.main.MainActivity", "auto_grant_permissions": ' \
               + 'true, "full_reset": true, "no_reset": false}, "java_path": ' + f'"{cl_path}"' + ', "udid": ' \
                                                                                                  '"emulator-5554", ' \
                                                                                                  '"api": ""}'

set_left_swipe = '{"apk": ' + f'"{apk_path}"' + ', "caps": {"app_wait_activity": ' \
                                                '"com.maltaisn.notes.ui.main.MainActivity", "auto_grant_permissions": ' \
                 + 'true, "full_reset": true, "no_reset": false}, "java_path": ' + f'"{sls_path}"' + ', "udid": ' \
                                                                                                     '"emulator-5554' \
                                                                                                     '", "api": ""}'

# Ensure proper escape sequences for file paths
create_label = create_label.replace("\\", "\\\\")
set_left_swipe = set_left_swipe.replace("\\", "\\\\")

# Define profile names
create_label_name = "EX_NOTES_CreateLabel"
set_left_swipe_name = "EX_NOTES_SetLeftSwipeToDe"


def create_examples():
    """
    Creates example profile directories and profile.json files if they do not already exist.

    The function checks if the profile directories for `create_label_name` and `set_left_swipe_name`
    exist inside `profile_path`. If they do not exist, it creates them and writes respective JSON content
    to a `profile.json` file inside each directory.
    """
    if os.path.exists(os.path.join(profile_path, create_label_name)) and os.path.exists(
            os.path.join(profile_path, set_left_swipe_name)):
        return

    # Create folders for each profile inside the profiles directory
    os.makedirs(os.path.join(profile_path, create_label_name), exist_ok=True)
    os.makedirs(os.path.join(profile_path, set_left_swipe_name), exist_ok=True)

    # Create and write profile.json files in respective directories
    with open(os.path.join(profile_path, create_label_name, "profile.json"), "w") as f:
        f.write(create_label)

    with open(os.path.join(profile_path, set_left_swipe_name, "profile.json"), "w") as f:
        f.write(set_left_swipe)


if __name__ == "__main__":
    create_examples()
