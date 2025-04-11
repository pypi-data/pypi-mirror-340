import time

from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.wait import WebDriverWait
from test2va.const import FIND_ELEMENT_WAIT
from selenium.webdriver.support import expected_conditions as ec

from test2va.util import camel_to_snake

from test2va.parser.util.literal_format_check import format_string_literal, format_number_literal

from ...parser.types.NewGrammar import ActionData, clickType


class EspressoActions:
    """Class containing methods for performing Espresso actions in Appium tests."""
    @staticmethod
    def action_on_item_at_position(element: WebElement, action: ActionData, driver: WebDriver, xpath: str):
        """Performs an action on an item at a specific position in a list.

        Args:
            element (WebElement): The parent element containing child elements.
            action (ActionData): The action data containing position and action details.
            driver (WebDriver): The WebDriver instance.
            xpath (str): The XPath used to locate child elements.

        Raises:
            IndexError: If the specified position is out of bounds.
        """
        position = int(format_number_literal(action["Args"][0][0]))
        nested_action: ActionData = action["Args"][1][0]

        # Get all child elements of the parent element
        child_elements = element.find_elements("xpath", f".{xpath}/child::*")

        if position < 0 or position >= len(child_elements):
            raise IndexError(f"Position {position} is out of bounds for child elements")

        # Get the child element at the specified position
        element_child = child_elements[position]

        action = getattr(EspressoActions, camel_to_snake(nested_action["Name"]))
        action(element_child, nested_action, driver, xpath)

    @staticmethod
    def clear_text(element: WebElement, _action: ActionData, _driver: WebDriver, xpath: str):
        """
        Clears the text of the given element.

        Args:
            element (WebElement): The element whose text needs to be cleared.
            _action (ActionData): The action data (not used in this method).
            _driver (WebDriver): The WebDriver instance (not used in this method).
            xpath (str): The XPath of the element (not used in this method).
        """
        element.clear()

    @staticmethod
    # TODO: Support int,int args and ViewAction in arg 0 for click
    def click(element: WebElement, _action: ActionData, _driver: WebDriver, xpath: str):
        """Clicks on the given element.

        Args:
            element (WebElement): The element to click on.
            _action (ActionData): The action data (not used in this method).
            _driver (WebDriver): The WebDriver instance (not used in this method).
            xpath (str): The XPath of the element (not used in this method).
        """
        element.click()

    @staticmethod
    def close_soft_keyboard(_element: WebElement, _action: ActionData, driver: WebDriver, xpath: str):
        """Closes the soft keyboard.

        Args:
            _element (WebElement): The element (not used in this method).
            _action (ActionData): The action data (not used in this method).
            driver (WebDriver): The WebDriver instance.
            xpath (str): The XPath of the element (not used in this method).
        """
        driver.hide_keyboard()

    @staticmethod
    def long_click(element: WebElement, _action: ActionData, driver: WebDriver, xpath: str):
        """Performs a long click on the given element.

        Args:
            element (WebElement): The element to long click on.
            _action (ActionData): The action data (not used in this method).
            driver (WebDriver): The WebDriver instance.
            xpath (str): The XPath of the element (not used in this method).
        """

        # Create a touch input source
        touch_input = PointerInput("touch", name="finger1")

        # Create action builder
        actions = ActionBuilder(driver, mouse=touch_input)

        # Move to the element and perform a long press
        actions.pointer_action.move_to(element)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(1)  # Pause for 1 second to simulate long press
        actions.pointer_action.pointer_up()

        # Perform the action
        actions.perform()

    @staticmethod
    def press_back(_element: WebElement, _action: ActionData, driver: WebDriver, xpath: str):
        """Presses the back button on the device.

        Args:
            _element (WebElement): The element (not used in this method).
            _action (ActionData): The action data (not used in this method).
            driver (WebDriver): The WebDriver instance.
            xpath (str): The XPath of the element (not used in this method).
        """
        time.sleep(1)
        driver.press_keycode(4)
        time.sleep(0.5)

    @staticmethod
    def press_ime_action_button(element: WebElement, _action: ActionData, driver: WebDriver, xpath: str):
        """Presses the IME action button (Enter or Done).

        Args:
            element (WebElement): The element (not used in this method).
            _action (ActionData): The action data (not used in this method).
            driver (WebDriver): The WebDriver instance.
            xpath (str): The XPath of the element (not used in this method).
        """
        #66: Enter or Done
        #84: Search
        #5: Next
        driver.press_keycode(66)
        #driver.press_keycode(84)

    @staticmethod
    def scroll_to(element: WebElement, action: ActionData, driver: WebDriver, xpath: str):
        """Scrolls to the given element until it is visible.

        Args:
            element (WebElement): The element to scroll to.
            action (ActionData): The action data containing scroll parameters.
            driver (WebDriver): The WebDriver instance.
            xpath (str): The XPath of the element (not used in this method).

        Raises:
            NoSuchElementException: If the element is not found after scrolling.
        """
        from ..util.find_xml_element import find_xml_element
        def perform_swipe():
            """Performs a swipe action to scroll the screen."""
            # Perform the swipe action if the element is not visible
            window_size = driver.get_window_size()
            width = window_size['width']
            height = window_size['height']

            # Calculate swipe start and end points
            start_x = width / 2
            start_y = height * 0.7  # Near the bottom
            end_x = start_x
            end_y = height * 0.3  # Near the top

            # Create touch input source
            touch_input = PointerInput("touch", name="finger1")

            # Create action builder
            actions = ActionBuilder(driver, mouse=touch_input)

            # Build the swipe action
            actions.pointer_action.move_to_location(start_x, start_y)
            actions.pointer_action.pointer_down()
            actions.pointer_action.pause(0.1)  # Short pause to mimic human interaction
            actions.pointer_action.move_to_location(end_x, end_y)
            actions.pointer_action.release()

            # Perform the action
            actions.perform()

        MAX_SCROLLS = 5  # Maximum number of scrolls to attempt
        # TODO: If this isn't reliable update the page source and check if it is visible
        if len(action["Args"]) == 0:
            for _ in range(MAX_SCROLLS):
                try:
                    if element.is_displayed():
                        # Get element's location and size
                        element_location = element.location
                        element_size = element.size

                        # Get the size of the device screen
                        window_size = driver.get_window_size()
                        screen_height = window_size['height']

                        # Check if the element's top and bottom are within the visible screen bounds
                        element_top = element_location['y']
                        element_bottom = element_top + element_size['height']

                        if 0 <= element_top <= screen_height and 0 <= element_bottom <= screen_height:
                            return  # Element is within the visible portion of the screen

                except (NoSuchElementException, StaleElementReferenceException):
                    pass

                perform_swipe()

            raise NoSuchElementException(f"Element not found within {MAX_SCROLLS} scrolls.")
        else:
            targ_selector = action["Args"][0][0]['Matchers'][0]
            for _ in range(MAX_SCROLLS):
                matched_element, xpath, tot_elements = find_xml_element(driver, targ_selector, element)

                if matched_element is None:
                    print("Element not found during scrollto")
                    perform_swipe()
                    continue

                try:
                    wait = WebDriverWait(driver, FIND_ELEMENT_WAIT)
                    element = wait.until(ec.presence_of_element_located((AppiumBy.XPATH, xpath)))
                except (TimeoutException, NoSuchElementException):
                    print(f"Element not found during scrollto: {xpath}")
                    perform_swipe()
                    continue

                if element.is_displayed():
                    # Get element's location and size
                    element_location = element.location
                    element_size = element.size

                    # Get the size of the device screen
                    window_size = driver.get_window_size()
                    screen_height = window_size['height']

                    # Check if the element's top and bottom are within the visible screen bounds
                    element_top = element_location['y']
                    element_bottom = element_top + element_size['height']

                    if 0 <= element_top <= screen_height and 0 <= element_bottom <= screen_height:
                        return

                perform_swipe()

    @staticmethod
    def sleep(_element: WebElement, action: ActionData, _driver: WebDriver, _xpath: str):
        """Pauses execution

        Args:
            _element (WebElement): The element (not used in this method).
            action (ActionData): The action data containing sleep duration.
            _driver (WebDriver): The WebDriver instance (not used in this method).
            _xpath (str): The XPath of the element (not used in this method).
        """
        tms = format_number_literal(action["Args"][0][0])
        tsecs = float(tms) / 1000
        time.sleep(tsecs)

    @staticmethod
    def swipe_left(element: WebElement, _action: ActionData, driver: WebDriver, xpath: str):
        """Swipes left on the given element.

        Args:
            element (WebElement): The element to swipe left on.
            _action (ActionData): The action data (not used in this method).
            driver (WebDriver): The WebDriver instance.
            xpath (str): The XPath of the element (not used in this method).
        """
        # Get the element location and size
        location = element.location
        size = element.size

        # Calculate start and end points for the swipe
        start_x = location['x'] + size['width'] * 0.8  # Near the right edge of the element
        end_x = location['x'] + size['width'] * 0.2  # Swipe left inside the element's bounds
        y = location['y'] + size['height'] / 2  # Vertically in the middle of the element

        # Create a touch input source
        touch_input = PointerInput("touch", name="finger1")

        # Create action builder
        actions = ActionBuilder(driver, mouse=touch_input)

        # Perform swipe action
        actions.pointer_action.move_to_location(start_x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(0.2)  # Wait for 200 ms
        actions.pointer_action.move_to_location(end_x, y)
        actions.pointer_action.pointer_up()

        # Perform the action
        actions.perform()

    @staticmethod
    def swipe_right(element: WebElement, _action: ActionData, driver: WebDriver, xpath: str):
        """Swipes right on the given element.

        Args:
            element (WebElement): The element to swipe right on.
            _action (ActionData): The action data (not used in this method).
            driver (WebDriver): The WebDriver instance.
            xpath (str): The XPath of the element (not used in this method).
        """
        # Get the element location and size
        location = element.location
        size = element.size

        # Calculate start and end points for the swipe
        start_x = location['x'] + size['width'] * 0.2  # Near the left edge of the element
        end_x = location['x'] + size['width'] * 0.8  # Swipe right inside the element's bounds
        y = location['y'] + size['height'] / 2  # Vertically in the middle of the element

        # Create a touch input source
        touch_input = PointerInput("touch", name="finger1")

        # Create action builder
        actions = ActionBuilder(driver, mouse=touch_input)

        # Perform swipe action
        actions.pointer_action.move_to_location(start_x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(0.2)  # Wait for 200 ms
        actions.pointer_action.move_to_location(end_x, y)
        actions.pointer_action.pointer_up()

        # Perform the action
        actions.perform()

    @staticmethod
    def replace_text(element: WebElement, action: ActionData, _driver: WebDriver, xpath: str):
        """Replaces the text in the given element.

        Args:
            element (WebElement): The element to replace text in.
            action (ActionData): The action data containing new text.
            _driver (WebDriver): The WebDriver instance (not used in this method).
            xpath (str): The XPath of the element (not used in this method).
        """
        text = format_string_literal(action["Args"][0][-1])
        element.clear()
        element.send_keys(text)

    @staticmethod
    def type_text(element: WebElement, action: ActionData, _driver: WebDriver, xpath: str):
        """Types text into the given element.

        Args:
            element (WebElement): The element to type text into.
            action (ActionData): The action data containing text to type.
            _driver (WebDriver): The WebDriver instance (not used in this method).
            xpath (str): The XPath of the element (not used in this method).
        """
        text = format_string_literal(action["Args"][0][-1])
        element.send_keys(text)


class EspressoActionsOld:
    @staticmethod
    def click(element: WebElement, _action: ActionData, _driver: WebDriver):
        element.click()

    @staticmethod
    def close_soft_keyboard(_element: WebElement, action: ActionData, driver: WebDriver):
        driver.hide_keyboard()

    @staticmethod
    def long_click(element: WebElement, _action: ActionData, driver: WebDriver):
        # Deprecated method using ActionChains
        pass  # This method is deprecated and should not be used

    @staticmethod
    def press_ime_action_button(element: WebElement, action: ActionData, driver: WebDriver):
        driver.press_keycode(66)

    @staticmethod
    def press_back(element: WebElement, action: ActionData, driver: WebDriver):
        driver.press_keycode(4)

    @staticmethod
    def replace_text(element: WebElement, action: ActionData, driver: WebDriver):
        element.clear()
        element.send_keys(action["args"][0]["content"])

    @staticmethod
    def type_text(element: WebElement, action: ActionData, driver: WebDriver):
        element.send_keys(action["args"][0]["content"])
