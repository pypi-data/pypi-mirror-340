from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from ...const.const import FIND_ELEMENT_WAIT
from ..util.build_xpath_from_element import build_xpath_from_element
from ..util.execute_action import execute_action
from ..util.find_xml_element import find_xml_element
from ...parser.types.LibTypes import ParsedData
from selenium.webdriver.support import expected_conditions as ec

from ...parser.types.NewGrammar import ParseData


def setup_test(driver: WebDriver, data: ParseData, second=False):
    """Executes the setup steps defined in the test's `Before` section.

    This function locates UI elements based on selectors, waits for them if necessary,
    and executes setup actions before the main test begins.

    Args:
        driver (WebDriver): The Appium WebDriver instance.
        data (ParseData): The parsed test data containing setup instructions.
        second (bool, optional): If `True`, retries finding elements if they are not
                                 found on the first attempt (useful for handling loading screens).
                                 Defaults to `False`.

    Raises:
        SystemExit: If an essential element is not found or an action fails, the test setup is aborted.
    """
    test_func_selectors = data["Before"]

    for selector in test_func_selectors:
        # Attempt to find corresponding XML element given by the selector criteria.
        matched_element, xpath, _ = find_xml_element(driver, selector)

        # This deals with loading. If it worked the first time, it must work again.
        while second and matched_element is None:
            matched_element, xpath, _ = find_xml_element(driver, selector)

        if matched_element is None:
            print("Element not found during test setup execution.")
            print("Test Setup Failed.")
            exit(1)

        element = None
        # We are going to find the element via xpath and execute the action on it to run through the test setup.
        try:
            wait = WebDriverWait(driver, FIND_ELEMENT_WAIT)
            element = wait.until(ec.presence_of_element_located((AppiumBy.XPATH, xpath)))
        except (TimeoutException, NoSuchElementException):
            print(f"Element not found during test setup execution: {xpath}")
            #print("Test Setup Failed.")
            #exit(1)

        try:
            execute_action(driver, element, xpath, selector["Action"])
        except Exception as e:
            print(f"Error executing test setup action: {e}")
            print("Test Setup Failed.")
            exit(1)
