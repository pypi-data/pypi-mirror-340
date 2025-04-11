from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver

from test2va.parser.util.literal_format_check import format_string_literal
from test2va.util import camel_to_snake

from test2va.parser.types.NewGrammar import ActionData


class EspressoAssertions:
    """Contains assertion methods for verifying UI elements using Espresso framework."""
    @staticmethod
    def matches(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Evaluates a nested assertion on the given element.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function to evaluate the assertion.
        """
        nested: ActionData = assertion["Args"][0][0]

        def f():
            return getattr(EspressoAssertions, camel_to_snake(nested["Name"]))(element, nested, driver)

        return f

    @staticmethod
    def _not(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Negates a nested assertion.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function to evaluate the negated assertion.
        """
        nested: ActionData = assertion["Args"][0][0]

        def f():
            return not getattr(EspressoAssertions, camel_to_snake(nested["Name"]))(element, nested, driver)

        return f

    @staticmethod
    def does_not_exist(element: WebElement, assertion: ActionData, driver: WebDriver):
        """This is a dummy method as doesNotExist is handled as a special case. This is here to avoid errors.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that always returns False.
        """
        def f():
            return False

        return f

    @staticmethod
    def is_checked(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element is selected (checked).

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the element is checked.
        """
        def f():
            return element.is_selected()

        return f

    @staticmethod
    def is_clickable(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element is clickable.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the element is clickable.
        """
        def f():
            if not element.is_enabled():
                return False
            if not element.is_displayed():
                return False
            if element.get_attribute("clickable") is not None and element.get_attribute("clickable") == "true":
                return True

            return False

        return f

    @staticmethod
    def is_displayed(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element is displayed on the screen.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the element is displayed.
        """
        def f():
            return element.is_displayed()

        return f

    @staticmethod
    def is_enabled(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element is enabled.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the element is enabled.
        """
        def f():
            return element.is_enabled()

        return f

    @staticmethod
    def is_not_checked(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element is not selected (unchecked).

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the element is not checked.
        """
        def f():
            return not element.is_selected()

        return f

    @staticmethod
    def is_not_clickable(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element is not clickable.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the element is not clickable.
        """
        def f():
            if not element.is_enabled():
                return True
            if not element.is_displayed():
                return True
            if element.get_attribute("clickable") is not None and element.get_attribute("clickable") == "false":
                return True

            return False

        return f

    @staticmethod
    def with_content_description(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element's content description matches the expected value.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data containing expected content description.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the content description matches.
        """
        content_arr = assertion["Args"][0]
        content = format_string_literal(content_arr[-1])

        def f():
            return content == element.get_attribute("contentDescription")

        return f

    @staticmethod
    def with_substring(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element's text contains a specified substring.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data containing the substring.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the text contains the substring.
        """
        text_arr = assertion["Args"][0]
        text = format_string_literal(text_arr[-1])

        def f():
            return text in element.text

        return f

    @staticmethod
    def with_text(element: WebElement, assertion: ActionData, driver: WebDriver):
        """Checks if an element's text matches the expected value.

        Args:
            element (WebElement): The target UI element.
            assertion (ActionData): The assertion data containing the expected text.
            driver (WebDriver): The WebDriver instance.

        Returns:
            function: A callable function that returns True if the text matches.
        """
        text_arr = assertion["Args"][0]
        text = format_string_literal(text_arr[-1])  # Only supports text argument for now

        def f():
            return text == element.text

        return f
