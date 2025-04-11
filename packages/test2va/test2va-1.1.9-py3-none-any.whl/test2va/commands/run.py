from test2va.bridge import check_file_exists, find_profile
from test2va.bridge.appium import find_running_device, get_capability_options
from test2va.execute import ToolExec


def _on_error(msg, _err):
    """Handles error messages during execution.

    Args:
        msg (str): Error message to display.
        _err: Additional error details (unused).

    Returns:
        None
    """
    print(f"❌ {msg}\n")


def _on_log(msg):
    """Handles log messages during execution.

    Args:
        msg (str): Log message to display.

    Returns:
        None
    """
    print(f"ℹ️ {msg}")


def _on_progress(msg):
    """Handles progress updates during execution.

    Args:
        msg (str): Progress message to display.

    Returns:
        None
    """
    print(f"ℹ️ {msg}\n")


def _on_success(msg):
    """Handles success messages during execution.

    Args:
        msg (str): Success message to display.

    Returns:
        None
    """
    print(f"✅ {msg}\n")


def _on_finish():
    """Handles completion of execution.

    Returns:
        None
    """
    print("🛑 Execution Stopped\n")


def run_command(args):
    """Executes the Test2VA tool using a specified profile and device.

    Args:
        args: Command-line arguments containing:
            - prof (str): Profile name.
            - udid (str, optional): Unique device identifier (UDID) of the device.
            - auto_udid (bool, optional): Whether to automatically detect a connected device.

    Returns:
        None
    """
    udid = args.udid

    if not args.prof:
        print(
            "Please provide a profile name with --prof. You can create a profile using 'test2va profile create <name>'")
        return

    prof = find_profile(args.prof)

    if not prof:
        print(f"Profile '{args.prof}' not found. You can create a profile using 'test2va profile create <name>'")
        return

    apk = prof["apk"]
    caps = prof["caps"]
    j_path = prof["java_path"]

    if not udid and args.auto_udid:
        devices = find_running_device()
        udid = udid if len(devices) <= 0 else devices[0]

    if not udid and not args.auto_udid:
        udid = prof["udid"]

    if not udid:
        print("Please provide a device UDID through the flag or a profile. If auto-udid was specified, make sure the "
              "device is running or provide the UDID manually with --udid. You can use 'adb devices' to check the "
              "connected devices.")
        return

    if not check_file_exists(apk):
        print(f"APK file not found. Please check the path in the profile. ({apk})")
        return

    if not check_file_exists(j_path):
        print(f"Java file not found. Please check the path in the profile. ({j_path})")
        return

    # Initialize and configure the execution tool
    Exe = ToolExec(
        udid=udid,
        apk=apk,
        added_caps=caps,
        cap_data=get_capability_options(),
        j_path=j_path,
        j_code=None
    )

    # Connect event handlers
    Exe.events.on_error.connect(_on_error)
    Exe.events.on_log.connect(_on_log)
    Exe.events.on_progress.connect(_on_progress)
    Exe.events.on_success.connect(_on_success)
    Exe.events.on_finish.connect(_on_finish)

    # Execute the tool
    Exe.execute()
