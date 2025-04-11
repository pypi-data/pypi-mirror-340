from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from ...const.const import FIND_ELEMENT_WAIT
from ..util.build_xpath_from_element import build_xpath_from_element
from ..util.find_xml_element import find_xml_element
from ...parser.types.LibTypes import SelectorData
from ...parser.types.NewGrammar import MatcherData, AssertionData


def find_element(driver: WebDriver, selector: MatcherData | AssertionData) -> (WebElement, str):
    """Finds an element using the provided selector and returns the WebElement along with its XPath.

    Args:
        driver (WebDriver): The Appium WebDriver instance.
        selector (Union[MatcherData, AssertionData]): A selector containing matching criteria.

    Returns:
        tuple[WebElement, str]: A tuple containing the found WebElement and its corresponding XPath.

    Raises:
        NoSuchElementException: If the element cannot be found.
    """
    matched_element, xpath, _ = find_xml_element(driver, selector)

    if matched_element is None:
        raise NoSuchElementException("Could not find element in base test.")

    wait = WebDriverWait(driver, FIND_ELEMENT_WAIT)
    return wait.until(ec.presence_of_element_located((AppiumBy.XPATH, xpath))), xpath
