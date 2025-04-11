from typing import List
from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver

from ..mappings.maps import ActionMap
from ...parser.types.NewGrammar import ActionData
from ...util.camel_to_snake import camel_to_snake


def execute_action(driver: WebDriver, element: WebElement, xpath: str, actions: List[ActionData]):
    """Executes a list of UI actions on a specified element using Espresso.

    Args:
        driver (WebDriver): The Appium WebDriver instance.
        element (WebElement): The target UI element on which the actions will be performed.
        xpath (str): The XPath of the element.
        actions (List[ActionData]): A list of actions to be executed on the element.

    Returns:
        None
    """
    library = "Espresso"

    for action in actions:
        getattr(ActionMap[library], camel_to_snake(action["Name"]))(element, action, driver, xpath)
