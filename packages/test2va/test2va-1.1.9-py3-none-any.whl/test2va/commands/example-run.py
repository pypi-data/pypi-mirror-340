import time
from appium.options.android import UiAutomator2Options

from test2va.bridge import start_server, parse, wait_app_load, validate_mutation
from test2va.bridge.examples import get_example_data
from test2va.bridge.tool import generate_va_methods


def example_run_command(args):
    """Executes an example run command using Appium and Test2VA.

    Args:
        args: Parsed command-line arguments containing:
            - example (str): The name of the example to run.
            - appium_url (str): The URL of the Appium server.
            - udid (str): The unique device identifier (UDID) of the target device.

    Returns:
        None

    Raises:
        None
    """
    example = args.example
    appium_url = args.appium_url
    udid = args.udid

    example_data = get_example_data(example)
    if example_data is None:
        return

    # Configure Appium options
    options = UiAutomator2Options()
    options.udid = udid
    options.app_wait_activity = example_data['app_activity']
    options.auto_grant_permissions = True
    options.no_reset = False
    options.full_reset = True
    options.app = example_data['app_path']

    # Start Appium server and establish connection with the device
    driver = start_server(appium_url, options)

    start = time.time()

    # Parse Java file
    data, java_file_name = parse(example_data['java_path'], driver)

    # Wait for the app to load before proceeding
    wait_app_load()

    # Perform mutation operations
    validate_mutation(driver, data, start, java_file_name)

    # Generate the required output
    generate_va_methods(driver)
