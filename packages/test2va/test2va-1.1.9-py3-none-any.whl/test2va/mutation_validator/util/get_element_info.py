from appium.webdriver import WebElement


def get_element_info(e: WebElement, xpath: str) -> dict:
    """Retrieves key attributes and state information of a given WebElement.

    Args:
        e (WebElement): The Appium WebElement whose attributes are to be retrieved.
        xpath (str): The XPath of the WebElement.

    Returns:
        dict: A dictionary containing the element's attributes and state information, including:
            - "xpath": (str) The element's XPath.
            - "displayed": (bool) Whether the element is visible on the screen.
            - "content-desc": (str | None) The element's content description.
            - "resource-id": (str | None) The element's resource ID.
            - "text": (str | None) The text content of the element.
            - "checked": (str | None) Whether the element is checked (if applicable).
            - "enabled": (str | None) Whether the element is enabled.
            - "selected": (str | None) Whether the element is selected.
    """
    return {
        "xpath": xpath,
        "displayed": e.is_displayed(),
        "content-desc": e.get_attribute("content-desc"),
        "resource-id": e.get_attribute("resource-id"),
        "text": e.get_attribute("text"),
        "checked": e.get_attribute("checked"),
        "enabled": e.get_attribute("enabled"),
        "selected": e.get_attribute("selected"),
    }
