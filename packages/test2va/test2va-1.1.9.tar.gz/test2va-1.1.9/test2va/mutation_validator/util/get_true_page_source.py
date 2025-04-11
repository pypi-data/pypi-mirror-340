import time

from appium.webdriver.webdriver import WebDriver
from selenium.common import StaleElementReferenceException

from ...const.const import FIND_ELEMENT_WAIT


def get_static_page_source(driver: WebDriver):
    """Retrieves a stable page source from the WebDriver, ensuring that the page has fully loaded.

    This function repeatedly checks the page source and waits until it stabilizes or
    until the maximum wait time (`FIND_ELEMENT_WAIT`) is reached.

    Args:
        driver (WebDriver): The Appium WebDriver instance.

    Returns:
        str: The static page source in XML format.

    Raises:
        StaleElementReferenceException: If the page updates in the middle of retrieval, it will retry.
    """
    previous_page_src = ""
    current_page_src = driver.page_source
    start_time = time.time()
    while current_page_src == previous_page_src and time.time() - start_time < FIND_ELEMENT_WAIT:
        time.sleep(0.5)  # Short sleep to avoid hammering the server
        previous_page_src = current_page_src
        try:
            current_page_src = driver.page_source
        except StaleElementReferenceException:
            # This exception might occur if the page is in the middle of an update
            pass

    return current_page_src
