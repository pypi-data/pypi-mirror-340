import re

from test2va.va_method_generator.core.supported_espresso_apis import SUPPORTED_MATCHERS, SUPPORTED_ACTIONS, SUPPORTED_NON_ESPRESSO
from test2va.va_method_generator.exceptions.exceptions import UnsupportedMatcherException, UnsupportedActionException


def validate_espresso_statement(espresso_statement: str) -> bool:
    """Validates an Espresso statement by checking whether all matchers and actions are supported.

    Args:
        espresso_statement (str): Raw Espresso statement as a string.

    Raises:
        UnsupportedMatcherException: If an unsupported matcher is found.
        UnsupportedActionException: If an unsupported action is found.

    Returns:
        bool: True if the statement is valid, otherwise raises an exception.
    """

    # Step 1: Handle special cases for `isRoot()`
    if espresso_statement.strip() == 'onView(isRoot()).perform(swipeLeft());':
        return True  # Special case is valid

    if espresso_statement.strip() == 'onView(isRoot()).perform(swipeRight());':
        return True  # Special case is valid

    # Step 2: Separate the `onView(...)` and `.perform(...)` parts
    match = re.match(r'(.+?)\.perform\((.+?)\);', espresso_statement.strip())
    if not match:
        raise ValueError(f"Invalid format. Ensure the statement follows the Espresso syntax: {espresso_statement}")

    on_view_part, perform_part = match.groups()

    # Step 3: Validate Matchers
    matchers = re.findall(r'(\w+)\(', on_view_part)  # Extract all function names inside `onView(...)`

    unsupported_matchers = [matcher for matcher in matchers if matcher not in SUPPORTED_MATCHERS]
    if unsupported_matchers:
        raise UnsupportedMatcherException(unsupported_matchers)

    # Step 4: Validate Actions
    actions = re.findall(r'(\w+)\(', perform_part)  # Extract all function names inside `.perform(...)`

    unsupported_actions = [action for action in actions if action not in SUPPORTED_ACTIONS]
    if unsupported_actions:
        raise UnsupportedActionException(unsupported_actions)

    return True  # Return True if everything is valid


def validate_non_espresso_statement(statement: str) -> bool:
    """
    Validates a non-Espresso statement by checking whether the APIs are supported.
    :param statement: a non-Espresso statement
    :return: True if supported.
    """
    # Remove leading/trailing spaces
    statement = statement.strip()

    # Directly check against the supported set
    if statement in SUPPORTED_NON_ESPRESSO:
        return True

    # Check if the statement follows the "Thread.sleep(X)" pattern
    if re.fullmatch(r"\s*Thread\.sleep\(\d+\);\s*", statement):
        return True

    return False


def convert_espresso_to_findNode(espresso_statement):
    """
    Converts a Java Espresso statement into a self-defined statement.

    Examples:

    Example 1: Basic Click Action
    -------------------------------------
    Input:
        espresso_statement = 'onView(allOf(withId(R.id.loginButton), withText("Login"))).perform(click());'

    Output:
        'performClick(findNode(withId("loginButton"), withText("Login")));'

    Example 2: Swiping Left on an Element
    -------------------------------------
    Input:
        espresso_statement = 'onView(allOf(withId(R.id.swipeableItem), withText("Item 1"))).perform(swipeLeft());'

    Output:
        'performSwipeLeftOnNode(findNode(withId("swipeableItem"), withText("Item 1")));'

    Example 3: Input Text
    -------------------------------------
    Input:
        espresso_statement = 'onView(allOf(withId(R.id.usernameField))).perform(typeText("testUser"));'

    Output:
        'performInput(findNode(withId("usernameField")), "testUser");'

    :param espresso_statement: A string representing the Java Espresso UI testing statement.
    :return: A string representing the converted Test2VA statement.
    """

    # Step 0: Handle special cases where `onView(isRoot())`
    if espresso_statement.strip() == 'onView(isRoot()).perform(swipeLeft());':
        return "performSwipeLeft();"

    if espresso_statement.strip() == 'onView(isRoot()).perform(swipeRight());':
        return "performSwipeRight();"

    # Step 1: Separate the `onView(...)` and `.perform(...)` parts
    match = re.match(r'(.+?)\.perform\((.+?)\);', espresso_statement.strip())
    if not match:
        return "Error: Invalid input format"

    on_view_part, perform_part = match.groups()

    # Step 2: Remove `isDisplayed()` cleanly (including commas if necessary)
    on_view_part = re.sub(r',?\s*isDisplayed\(\)', '', on_view_part)

    # Step 3: Convert `withId(R.id.X)` → `withId("X")`
    on_view_part = re.sub(r'withId\(R\.id\.(\w+)\)', r'withId("\1")', on_view_part)

    # Step 4: Convert `withId(android.R.id.X)` → `withId("X")`
    on_view_part = re.sub(r'withId\(android\.R\.id\.(\w+)\)', r'withId("\1")', on_view_part)

    # Step 5: Remove `allOf(...)` while maintaining correct argument structure
    on_view_part = re.sub(r'allOf\((.*?)\)', r'\1', on_view_part)

    # Step 6: Replace `onView(...)` with `findNode(...)`
    on_view_part = re.sub(r'onView\((.*?)\)', r'findNode(\1)', on_view_part)

    # Step 7: Convert `.perform(replaceText(X))` or `.perform(typeText(X))` to `performInput(findNode(...), X)`
    text_match = re.search(r'(?:replaceText|typeText)\(([^)]+)\)', perform_part)  # Match anything inside replaceText()
    if text_match:
        text_value = text_match.group(1)  # Capture the value inside replaceText()
        return f'performInput({on_view_part}, {text_value});'  # No quotes added to preserve variable usage

    # Step 8: Convert `.perform(click());` to `performClick(findNode(...));`
    if perform_part.strip() == "click()":
        return f"performClick({on_view_part});"

    # Step 9: Convert `.perform(swipeLeft());` to `performSwipeLeftOnNode(findNode(...));`
    if perform_part.strip() == "swipeLeft()":
        return f"performSwipeLeftOnNode({on_view_part});"

    # Step 10: Convert `.perform(swipeRight());` to `performSwipeRightOnNode(findNode(...));`
    if perform_part.strip() == "swipeRight()":
        return f"performSwipeRightOnNode({on_view_part});"

    return f"{on_view_part}.perform({perform_part});"


def convert_espresso_statement(espresso_statement: str) -> str:
    """
    Convert the given espresso statement to the Test2VA statement.
    If invalid, will throw exception
    :param espresso_statement: espresso statement
    :return: Test2VA statement
    """
    if validate_espresso_statement(espresso_statement):
        return convert_espresso_to_findNode(espresso_statement)


if __name__ == '__main__':

    # Test Cases
    test_statements = [
        # 'onView(withId(R.id.button)).perform(click());',  # ✅ Supported
        # 'onView(allOf(withId(R.id.text), withText(heelo))).perform(swipeLeft());',  # ✅ Supported
        # 'onView(withId(R.id.button)).perform(doubleClick());',  # ❌ Unsupported action
        # 'onView(withRandomMatcher(R.id.button)).perform(click());',  # ❌ Unsupported matcher
        # 'onView(isRoot()).perform(swipeLeft());',  # ✅ Supported special case
        # 'onView(isRoot()).perform(swipeRight());',  # ✅ Supported special case
        # 'onView(allOf(withText("Press"), unsupportedMatcher())).perform(click());',  # ❌ Unsupported matcher
        # 'onView(allOf(withId(R.id.text_deck_name), withText(containsStringIgnoringCase("Keto Fruit")))).perform(click());',
        # 'onView(allOf(withId(R.id.button_edit), withParent(withParent(hasDescendant(withText(containsStringIgnoringCase("Blueberry"))))))).perform(click());',
        # 'onView(allOf(withContentDescription("Open drawer"), isDisplayed())).perform(click());'
        'onView(allOf(withId(R.id.category_name), isDisplayed())).perform(replaceText(param3));'

    ]

    for statement in test_statements:
        try:
            result = convert_espresso_statement(statement)
            print(f"{statement} => Valid: {result}")
        except UnsupportedMatcherException as e:
            print(f"{statement} => ERROR: {e}")
        except UnsupportedActionException as e:
            print(f"{statement} => ERROR: {e}")
        except ValueError as e:
            print(f"{statement} => ERROR: {e}")