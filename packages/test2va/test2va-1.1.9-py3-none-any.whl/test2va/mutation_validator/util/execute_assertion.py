from typing import List

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from test2va.util import camel_to_snake
from .find_xml_element import find_xml_element

from ..structs.EspressoAssertions import EspressoAssertions
from ...const.const import FIND_ELEMENT_WAIT
from ..util.build_xpath_from_element import build_xpath_from_element
from ..util.find_element import find_element
from appium.webdriver.webdriver import WebDriver

from ...parser.types.NewGrammar import AssertionData


# TODO: Implement other assertions other than exists.
def execute_assertion(driver: WebDriver, assertion_data: List[AssertionData]):

    for assertion in assertion_data:
        if assertion["Action"][0]["Name"] == "doesNotExist":
            element, xpath, _ = find_xml_element(driver, assertion)
            if element is None:
                # Assertion passes because the element is not found.
                continue
            else:
                # Element found when it should not exist.
                return False

        try:
            assertion_element, xpath = find_element(driver, assertion)
        except NoSuchElementException:
            return False

        wait = WebDriverWait(driver, FIND_ELEMENT_WAIT)

        # TODO: Formal assertion mapping
        try:
            element = wait.until(ec.presence_of_element_located((AppiumBy.XPATH, xpath)))

            if len(assertion["Action"]) == 0:
                return True

            assertion_func = getattr(EspressoAssertions, camel_to_snake(assertion["Action"][0]["Name"]))

            assertion_func(element, assertion["Action"][0], driver)()
        except TimeoutException:
            return False

    return True

