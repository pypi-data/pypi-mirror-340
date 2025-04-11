from typing import Union, Tuple

from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    InvalidSelectorException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from ...const.const import FIND_ELEMENT_WAIT
from ..util.find_xml_element import find_xml_element
from ...parser.types.NewGrammar import MatcherData, AssertionData


def find_ele_xpath_fallback(driver: WebDriver, xpath: str, selector: MatcherData | AssertionData) -> Union[Tuple[WebElement, str], Tuple[None, None]]:
    """Attempts to find an element using XPath first, then falls back to using a selector.

    Args:
        driver (WebDriver): The Appium WebDriver instance.
        xpath (str): The XPath string used to locate the element.
        selector (Union[MatcherData, AssertionData]): A selector data structure used as a fallback.

    Returns:
        Union[Tuple[WebElement, str], Tuple[None, None]]:
            - A tuple containing the located WebElement and its corresponding XPath if found.
            - `(None, None)` if no element is found.
    """
    wait = WebDriverWait(driver, FIND_ELEMENT_WAIT)

    # XPath first
    try:
        return wait.until(ec.presence_of_element_located((AppiumBy.XPATH, xpath))), xpath
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException, InvalidSelectorException):
        print(f"Couldn't find element with xpath. (find_ele_xpath_fallback) {xpath}")
        pass
        # Continue to selector

    # Selector data
    matched_element, xpath_selector, _ = find_xml_element(driver, selector)

    if matched_element is None:
        print("Couldn't find element with either xpath or selector. (find_ele_xpath_fallback)")
        return None, None

    try:
        return wait.until(ec.presence_of_element_located((AppiumBy.XPATH, xpath_selector))), xpath_selector
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        print("Couldn't find element with either xpath or selector. (find_ele_xpath_fallback)")
        return None, None
