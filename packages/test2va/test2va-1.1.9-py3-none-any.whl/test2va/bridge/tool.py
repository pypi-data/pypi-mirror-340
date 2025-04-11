import json
import os
import shutil
import subprocess
import time

from appium.webdriver.webdriver import WebDriver
from selenium.common import InvalidSelectorException

from test2va.va_method_generator.va_method_generator import generate_test2va_method_per_mutant_report
from test2va.mutation_validator.util.grant_permissions import grant_permissions
from test2va.mutation_validator.util.clear_user_data import clear_user_data
from test2va.mutation_validator.mutation_validator import mutation_validator
from test2va.parser.parser import parser
from test2va.mutation_validator import mutator
from test2va.exceptions import ParseError, MutatorError, GeneratorError
from test2va.util import write_json


def parse(app_file_path, java_file_path, driver: WebDriver, events):
    """Parses a Java file and stores the parsed output.

    Args:
        app_file_path (str): Path to the apk file.
        java_file_path (str): Path to the Java source file to be parsed.
        driver (WebDriver): Instance of Appium WebDriver.
        events: Event logging or tracking object.

    Returns:
        tuple: Parsed data and output path.

    Raises:
        ParseError: If there is an error parsing the Java file.
    """
    app_file_name = os.path.basename(app_file_path)[:os.path.basename(app_file_path).rfind(".")]

    try:
        date_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        output_path = os.path.join(os.path.dirname(__file__), "../output", f"{app_file_name}_{date_time}")

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        data = parser(os.path.join(output_path, "java_parsed.json"), java_file_path, events)

        return data, output_path
    except Exception as e:
        raise ParseError(f"Error parsing Java file: {java_file_path} - See console for details.", events)


max_tries = 3


def validate_mutation(driver: WebDriver, data: dict, start: float, ai_data, output_path: str, events, ai_callback,
                      auto_grant_perms=True):
    """Mutates the application using AI data and handles retry logic in case of errors.

    Args:
        driver (WebDriver): Instance of Appium WebDriver.
        data (dict): Parsed data from the Java file.
        start (float): Start time of the mutation process.
        ai_data: AI generated mutation data.
        output_path (str): Path where output files are stored.
        events: Event logging or tracking object.
        ai_callback: Callback function to retrieve AI data.
        auto_grant_perms (bool, optional): Whether to auto-grant permissions. Defaults to True.

    Returns:
        tuple: Output path and new AI data.

    Raises:
        MutatorError: If the mutation process fails.
    """
    tries = 1
    try:
        new_ai_data = mutation_validator(driver, data[0], ai_data, output_path, auto_grant_perms)
    except InvalidSelectorException as e:
        if tries == max_tries:
            raise MutatorError("Error mutating app - See console for details.", events)

        app_id = driver.current_package

        driver.terminate_app(app_id)
        clear_user_data(driver, app_id)
        grant_permissions(driver, app_id, auto_grant_perms)
        driver.activate_app(app_id)

        tries += 1
        print(f"Error mutating app - Retrying attempt {tries}...")
        ai_data = ai_callback()
        new_ai_data = mutation_validator(driver, data[0], ai_data, output_path, auto_grant_perms)
    except Exception as e:
        raise MutatorError("Error mutating app - See console for details.", events)

    return output_path, new_ai_data


def generate_va_methods(java_xml_path, ai_report_path, output_path, events):
    """Generates methods based on the mutated data.

    Args:
        java_xml_path (str): Path to the Java XML report.
        ai_report_path (str): Path to the AI report.
        output_path (str): Path where the generated report will be stored.
        events: Event logging or tracking object.

    Returns:
        str: Output path.

    Raises:
        GeneratorError: If the report generation fails.
    """
    try:
        generate_test2va_method_per_mutant_report(
            java_xml_path,
            ai_report_path,
            output_path
        )
    except Exception as e:
        raise GeneratorError("Error generating task methods - See console for details.", events)

    return output_path


def get_cap_type(caps, cap):
    """Retrieves the type of a given capability.

    Args:
        caps (list): List of capability tuples.
        cap (str): Capability name.

    Returns:
        str: Capability type.
    """
    for c in caps:
        if c[0] == cap:
            return c[1]


def format_caps(cap_cache: dict[str, str], cap_data) -> dict[str, str | int | bool]:
    """Formats capabilities based on their type.

    Args:
        cap_cache (dict): Cached capabilities.
        cap_data (list): Capability metadata.

    Returns:
        dict: Formatted capabilities.
    """
    caps = {}

    for cap, val in cap_cache.items():
        cap_type = get_cap_type(cap_data, cap)
        if not isinstance(cap_type, str):
            caps[cap] = val
        elif cap_type == "bool":
            caps[cap] = val.lower() == "true"
        elif cap_type == "int":
            caps[cap] = int(val)
        else:
            caps[cap] = val

    return caps


def check_node_installed():
    """Checks if Node.js is installed.

    Returns:
        bool: True if Node.js is installed, False otherwise.
    """
    try:
        subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_npm_installed():
    """Checks if npm is installed and returns its path.

    Returns:
        str: Path to npm if installed, None otherwise.
    """
    npm_path = shutil.which("npm")
    if npm_path is None:
        print("npm is not installed or not found in the system PATH.")
        return
    print(f"npm found at: {npm_path}")
    return npm_path


def check_npm_appium_install():
    """Checks if Appium is installed globally using npm.

    Returns:
        bool: True if Appium is installed, False otherwise.
    """
    npm_path = check_npm_installed()

    if npm_path is None:
        return False

    try:
        env = os.environ.copy()
        result = subprocess.run([npm_path, "list", "-g", "appium"], capture_output=True, text=True, env=env)
        return "appium" in result.stdout
    except subprocess.CalledProcessError:
        return False


def install_appium():
    """Installs Appium globally using npm.

    Returns:
        bool: True if installation is successful, False otherwise.
    """
    npm_path = check_npm_installed()
    if npm_path is None:
        return False

    try:
        env = os.environ.copy()
        subprocess.run([npm_path, "install", "-g", "appium"], check=True, text=True, capture_output=True, env=env)
        return True
    except subprocess.CalledProcessError:
        return False


def check_uia2_driver_install():
    """Checks if the UiAutomator2 driver is installed in Appium.

    Returns:
        bool: True if UiAutomator2 is installed, False otherwise.
    """
    appium_path = shutil.which("appium")

    if appium_path is None:
        print("Appium command not found in PATH.")
        return False

    try:
        env = os.environ.copy()
        result = subprocess.run([appium_path, "driver", "list", "--installed"], capture_output=True, text=True,
                                check=True, env=env)
        return "uiautomator2" in result.stdout or "uiautomator2" in result.stderr
    except subprocess.CalledProcessError:
        return False


def install_uia2_driver():
    """Installs the UiAutomator2 driver in Appium.

    Returns:
        bool: True if installation is successful, False otherwise.
    """
    appium_path = shutil.which("appium")

    if appium_path is None:
        print("Appium command not found in PATH.")
        return False

    try:
        env = os.environ.copy()
        subprocess.run([appium_path, "driver", "install", "uiautomator2"], capture_output=True, text=True, check=True,
                       env=env)
        return True
    except subprocess.CalledProcessError:
        return False
