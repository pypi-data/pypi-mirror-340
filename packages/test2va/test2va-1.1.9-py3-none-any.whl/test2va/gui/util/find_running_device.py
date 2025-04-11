import subprocess


def find_running_device():
    """Finds and returns a list of running Android devices using ADB.

    This function executes the `adb devices` command and extracts the list of connected devices.

    Returns:
        list: A list of device IDs (UDIDs) if devices are found, otherwise an empty list.
    """
    command = ["adb", "devices"]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout

    lines = output.split("\n")
    if len(lines) < 2:
        return []

    devices = []
    for line in lines[1:]:
        if not line:
            continue

        device = line.split("\t")[0]
        devices.append(device)

    return devices
