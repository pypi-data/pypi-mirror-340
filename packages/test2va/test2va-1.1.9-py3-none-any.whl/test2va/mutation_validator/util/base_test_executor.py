import os

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from ...const.const import FIND_ELEMENT_WAIT
from ..mappings.maps import TextActionMap
from ..util.build_xpath_from_element import build_xpath_from_element
from ..util.execute_action import execute_action
from ..util.find_xml_element import find_xml_element
from ..util.get_element_info import get_element_info
from ..util.populate_mutators import populate_mutators
from ...parser.types.LibTypes import ParsedData
from selenium.webdriver.support import expected_conditions as ec

from ...parser.types.NewGrammar import ParseData

WRITE_PG_SRC = True


def base_test_executor(mutators, driver: WebDriver, data: ParseData, element_count: list, base_path: list, output_path: str):
    """Executes a base test on UI elements by finding and interacting with them.

    Args:
        mutators (list): List to store mutators for elements.
        driver (WebDriver): The Appium WebDriver instance.
        data (ParseData): Parsed test data containing matchers and actions.
        element_count (list): List to store element counts encountered during execution.
        base_path (list): List to store element paths encountered.
        output_path (str): Directory to save test results.

    Returns:
        str or None: The path where page sources are saved, or None if not applicable.
    """
    test_func_selectors = data["Matchers"]
    idx = 0

    for selector in test_func_selectors:
        # Attempt to find corresponding XML element given by the selector criteria.
        matched_element, xpath, tot_elements = find_xml_element(driver, selector)

        if matched_element is None:
            print("Element not found during base test execution.")
            print("Base Test Failed.")
            exit(1)

        # We are going to find the element via xpath and execute the action on it to run through the base test.
        # At the same time we are going to populate the mutators.
        try:
            wait = WebDriverWait(driver, FIND_ELEMENT_WAIT)
            element = wait.until(ec.presence_of_element_located((AppiumBy.XPATH, xpath)))
        except (TimeoutException, NoSuchElementException):
            print(f"Element not found during base test execution: {xpath}")
            print("Base Test Failed.")
            exit(1)

        element_info = get_element_info(element, xpath)

        base_path.append(element_info)

        element_mutators = []

        mutators.append(element_mutators)

        text = None
        for action in selector["Action"]:
            if action["Name"] in TextActionMap:
                text = str(action["Args"][-1])
                break

        populate_mutators(driver, element_mutators, matched_element, text)

        if WRITE_PG_SRC:
            write_pg_src(driver, data, idx, output_path)
            idx += 1

        execute_action(driver, element, xpath, selector["Action"])

        element_count.append(tot_elements)

    if WRITE_PG_SRC:
        return write_pg_src(driver, data, "final", output_path)


def write_pg_src(driver: WebDriver, data: ParseData, event: int | str, path):
    """Saves the current page source as an XML file.

    Args:
        driver (WebDriver): The Appium WebDriver instance.
        data (ParseData): Parsed test data containing the test name.
        event (int | str): The event number or identifier for the page source.
        path (str): The directory where the XML file should be saved.

    Returns:
        str: The path of the folder where the page source is saved.
    """
    # If the folder 'pg_src' does not exist, create it.
    if not os.path.exists(os.path.join(path, "pg_src")):
        os.makedirs(os.path.join(path, "pg_src"))

    destination_folder = os.path.join(path, "pg_src")

    current_page_src = driver.page_source

    # Write the XML file to the folder 'pg_src/data["Name"]'.
    with open(os.path.join(destination_folder, f"{data['Name']}-event-{event}-xml-content.xml"), "w", encoding='utf-8') as f:
        f.write(current_page_src)

    return destination_folder
