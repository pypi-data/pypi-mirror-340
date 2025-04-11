from typing import List

from test2va.parser.util.literal_format_check import format_string_literal, format_number_literal

from .EspressoMatchTypes import EspressoMatchTypes
from ...parser.structs.XMLElement import XMLElement
from ...parser.types.LibTypes import CriteriaArgument, NestedCriteria
from appium.webdriver.webdriver import WebDriver

from ...parser.types.NewGrammar import childAtPositionType, MatcherData, isDisplayedType, withContentDescriptionType, \
    withTextType, withParentType, withIdType, isCheckedType, withChildType
from ...util.camel_to_snake import camel_to_snake


# TODO: Tests to do
# DL new myexpenses
# check out the two failed medtime

# TODO: Check out correlation_report folder
# TODO: Run some of the JSON tests (notes?)

# Diaguard changeWeightUnitTest didn't work

class EspressoCriteria:
    """Contains criteria matching functions for Espresso-based UI testing."""
    @staticmethod
    def child_at_position(args: childAtPositionType, driver: WebDriver, root: XMLElement):
        """Matches a child element at a specific position within a parent element.

        Args:
            args (childAtPositionType): The action arguments, including position and matcher details.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element of the UI tree.

        Returns:
            function: A callable function that evaluates whether an element matches the criteria.
        """
        nested_view_matcher: MatcherData = args[0][0]["Matchers"][0]
        position = int(args[1][0])

        funcs = []
        for component in nested_view_matcher["Components"]:
            func_name = camel_to_snake(component["Name"])
            func = getattr(EspressoCriteria, func_name)(component["Args"], driver=driver, root=root)
            funcs.append(func)

        nested_match_type = nested_view_matcher["MatchType"]
        parent_matcher = getattr(EspressoMatchTypes, nested_match_type)(funcs)

        def f(e: XMLElement) -> bool:
            parent = e.get_parent()

            if parent is None:
                return False

            if not parent_matcher(parent):
                return False

            # Check if the element is at the desired position
            children = parent.get_children()
            if len(children) > position and children[position] == e:
                return True

            return False

        return f

    @staticmethod
    def has_descendant_spec(args: withParentType, driver: WebDriver, root: XMLElement):
        """Alternate version of has_descendant that uses a different approach to match descendants.

        Args:
            args (withParentType): The action arguments, including matcher details.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element of the UI tree.

        Returns:
            function: A callable function that evaluates whether an element matches the criteria.
        """
        desc_criteria = args[0][0]["Matchers"][0]

        funcs = []
        for component in desc_criteria["Components"]:
            func_name = camel_to_snake(component["Name"])
            func = getattr(EspressoCriteria, func_name)(component["Args"], driver=driver, root=root)
            funcs.append(func)

        nested_match_type = desc_criteria["MatchType"]
        desc_match_type = getattr(EspressoMatchTypes, nested_match_type)(funcs)

        def f(e: XMLElement) -> bool:
            return desc_match_type(e)

        return f

    @staticmethod
    def has_descendant(args: withParentType, driver: WebDriver, root: XMLElement):
        """Matches elements that have a specific descendant.

        Args:
            args (withParentType): The arguments defining the descendant criteria.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that checks if an element has the specified descendant.
        """
        desc_criteria = args[0][0]["Matchers"][0]

        funcs = []
        for component in desc_criteria["Components"]:
            func_name = camel_to_snake(component["Name"])
            func = getattr(EspressoCriteria, func_name)(component["Args"], driver=driver, root=root)
            funcs.append(func)

        nested_match_type = desc_criteria["MatchType"]
        desc_match_type = getattr(EspressoMatchTypes, nested_match_type)(funcs)

        def f(e: XMLElement) -> bool:
            descendants = e.find_descendants(lambda _e: desc_match_type(_e))

            return len(descendants) > 0

        return f

    @staticmethod
    def is_checked(args: isCheckedType, driver: WebDriver, root: XMLElement):
        """Checks if an element is marked as checked.

        Args:
            args (isCheckedType): The action arguments (unused).
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element is checked.
        """
        def f(e: XMLElement) -> bool:
            checked = e.get("checked")

            if checked is None:
                return False

            return checked == "true"

        return f

    @staticmethod
    def is_not_checked(args: isCheckedType, driver: WebDriver, root: XMLElement):
        """Checks if an element is not marked as checked.

        Args:
            args (isCheckedType): The action arguments (unused).
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element is not checked.
        """
        def f(e: XMLElement) -> bool:
            checked = e.get("checked")

            if checked is None:
                return False

            return checked == "false"

        return f

    @staticmethod
    def is_displayed(args: isDisplayedType, driver: WebDriver, root: XMLElement):
        """Checks if an element is displayed.

        Args:
            args (isDisplayedType): The action arguments (unused).
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element is displayed.
        """
        def f(e: XMLElement) -> bool:
            return e.get("displayed") == "true"

        return f

    @staticmethod
    def is_enabled(args: isDisplayedType, driver: WebDriver, root: XMLElement):
        """Checks if an element is enabled.

        Args:
            args (isDisplayedType): The action arguments (unused).
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element is enabled.
        """

        def f(e: XMLElement) -> bool:
            return e.get("enabled") == "true"

        return f

    @staticmethod
    def is_root(args: isDisplayedType, driver: WebDriver, root: XMLElement):
        """Checks if an element is the root element.

        Args:
            args (isDisplayedType): The action arguments (unused).
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element is the root element.
        """

        def f(e: XMLElement) -> bool:
            return True

        return f

    @staticmethod
    def with_child(args: withChildType, driver: WebDriver, root: XMLElement):
        """Matches elements that have a specific child.

        Args:
            args (withChildType): The action arguments, including matcher details.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that checks if an element has the specified child.
        """

        child_criteria = args[0][0]["Matchers"][0]

        funcs = []
        for component in child_criteria["Components"]:
            func_name = camel_to_snake(component["Name"])
            func = getattr(EspressoCriteria, func_name)(component["Args"], driver=driver, root=root)
            funcs.append(func)

        nested_match_type = child_criteria["MatchType"]
        child_match_type = getattr(EspressoMatchTypes, nested_match_type)(funcs)

        def f(e: XMLElement) -> bool:
            children = e.get_children()
            return any(child_match_type(child) for child in children)

        return f

    @staticmethod
    def with_class_name(args: withContentDescriptionType, driver: WebDriver, root: XMLElement):
        """Checks if an element has a specific class name.

        Args:
            args (withContentDescriptionType): The action arguments containing the expected class name.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element has the expected class name.
        """

        text_arr = args[0]
        modifier = text_arr[0]
        text = format_string_literal(text_arr[-1])

        def f(e: XMLElement) -> bool:
            if modifier == "containsString":
                return text in e.tag
            if modifier == "is":
                return e.tag == text
            if modifier == "containsStringIgnoringCase":
                return text.lower() in e.tag.lower()
            return text.lower() in e.tag.lower()

        return f

    @staticmethod
    # TODO: Implement int and CharSequenceMatchers for withContentDescription
    def with_content_description(args: withContentDescriptionType, driver: WebDriver, root: XMLElement):
        """Checks if an element has a specific content description.

        Args:
            args (withContentDescriptionType): The action arguments containing the expected content description.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element has the expected content description.
        """
        text_arr = args[0]
        text = format_string_literal(text_arr[-1])  # Only supports text argument for now

        def f(e: XMLElement) -> bool:
            cd = e.get("content-desc")

            if cd is None:
                return False

            return e.get("content-desc") == text

        return f

    @staticmethod
    # TODO: Implement int and IntegerMatchers for withID
    def with_id(args: withIdType, driver: WebDriver, root: XMLElement):
        """Checks if an element has a specific resource ID.

        Args:
            args (withIdType): The action arguments containing the expected resource ID.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element has the expected resource ID.
        """
        text_arr = args[0]
        text = format_string_literal(text_arr[-1])

        def f(e: XMLElement) -> bool:
            rid = e.get("resource-id")

            if rid is None:
                return False

            current_pkg = driver.current_package
            id_format = text.split(".")[-1]
            return rid == f"{current_pkg}:id/{id_format}" or rid == f"android:id/{id_format}"

        return f

    @staticmethod
    def with_parent(args: withParentType, driver: WebDriver, root: XMLElement):
        """Checks if an element has a specific parent.

        Args:
            args (withParentType): The action arguments, including matcher details.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that checks if an element has the specified parent.
        """

        parent_criteria = args[0][0]["Matchers"][0]

        funcs = []
        for component in parent_criteria["Components"]:
            func_name = camel_to_snake(component["Name"])
            func = getattr(EspressoCriteria, func_name)(component["Args"], driver=driver, root=root)
            funcs.append(func)

        nested_match_type = parent_criteria["MatchType"]
        parent_matcher = getattr(EspressoMatchTypes, nested_match_type)(funcs)

        def f(e: XMLElement) -> bool:
            if e.get_parent() is None:
                return False

            return parent_matcher(e.get_parent())

        return f

    @staticmethod
    def with_parent_index(args: withParentType, driver: WebDriver, root: XMLElement):
        """Checks if an element has a specific parent at a specific index.

        Args:
            args (withParentType): The action arguments, including matcher details.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that checks if an element has the specified parent at the given index.
        """
        index = int(format_number_literal(args[0][0]))

        def f(e: XMLElement) -> bool:
            if e.get_parent() is None:
                return False

            children = e.get_parent().get_children()
            return len(children) > index and children[index] == e

        return f

    @staticmethod
    # TODO: Implement int and CharSequenceMatchers*** for withText*** needed for examples file
    def with_text(args: withTextType, driver: WebDriver, root: XMLElement):
        """Checks if an element has a specific text.

        Args:
            args (withTextType): The action arguments containing the expected text.
            driver (WebDriver): The WebDriver instance.
            root (XMLElement): The root XML element.

        Returns:
            function: A callable function that returns True if the element has the expected text.
        """

        text_arr = args[0]
        modifier = text_arr[0]
        text = format_string_literal(text_arr[-1])  # Only supports text argument for now

        def f(e: XMLElement) -> bool:
            if modifier == "containsString":
                return text in e.get("text")
            if modifier == "is":
                return e.get("text") == text
            if modifier == "containsStringIgnoringCase":
                return text.lower() in e.get("text").lower()
            return e.get("text") == text

        return f


class EspressoCriteriaOld:
    @staticmethod
    def all_of(arg: List[CriteriaArgument | NestedCriteria], driver: WebDriver, root: XMLElement):
        funcs = [getattr(EspressoCriteria, camel_to_snake(c["name"]))(c["args"], driver=driver, root=root) for c in arg]

        def f(e: XMLElement) -> bool:
            return all(func(e) for func in funcs)

        return f

    @staticmethod
    # TODO: Revisit this and fromParent, I don't understand these.
    def child_at_position(arg: List[CriteriaArgument | NestedCriteria], driver: WebDriver, root: XMLElement):
        parent_criteria = arg[0]

        # Check if parent_criteria is of type 'allOf'
        if parent_criteria.get("name") == "allOf":
            funcs = []
            for criterion in parent_criteria["args"]:
                func_name = camel_to_snake(criterion["name"])
                func = getattr(EspressoCriteria, func_name)(criterion["args"], driver=driver, root=root)
                funcs.append(func)

            def parent_matcher(parent: XMLElement) -> bool:
                return all(fun(parent) for fun in funcs)
        else:
            # Single criterion
            func_name = camel_to_snake(parent_criteria["name"])
            parent_matcher = getattr(EspressoCriteria, func_name)(parent_criteria["args"], driver=driver, root=root)

        # The second argument is the position within the parent
        position = int(arg[1]["content"])

        def f(e: XMLElement) -> bool:
            parent = e.get_parent()

            if parent is None:
                return False

            if not parent_matcher(parent):
                return False

            # Check if the element is at the desired position
            children = parent.get_children()
            if len(children) > position and children[position] == e:
                return True

            return False

        return f

    @staticmethod
    def contains_string_ignoring_case(arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement, referrer: str):
        text = arg[0]["content"]

        def f(e: XMLElement) -> bool:
            if referrer == "with_class_name":
                return text.lower() in e.tag.lower()
            if referrer == "with_text":
                return text.lower() in e.get("text").lower()

        return f

    @staticmethod
    def ends_with_ignoring_case(arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement, referrer: str):
        text = arg[0]["content"]

        def f(e: XMLElement) -> bool:
            if referrer == "with_class_name":
                return e.tag.lower().endswith(text.lower())

        return f

    @staticmethod
    # Special keyword is handled in camel_to_snake
    def _is(arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement, referrer: str):
        text = arg[0]["content"]

        def f(e: XMLElement) -> bool:
            if referrer == "with_class_name":
                return e.tag == text
            if referrer == "with_text":
                return e.get("text") == text

        return f

    @staticmethod
    def is_displayed(_arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement):
        return lambda e: e.get("displayed") == "true"

    @staticmethod
    def is_focused(_arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement):
        return lambda e: e.get("focused") == "true"

    @staticmethod
    def is_not_checked(_arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement):
        def f(e: XMLElement) -> bool:
            checked = e.get("checked")

            if checked is None:
                return False

            return checked == "false"

        return f

    @staticmethod
    def with_class_name(arg: List[CriteriaArgument | NestedCriteria], driver: WebDriver, root: XMLElement):
        matcher = arg[0]

        func_name = camel_to_snake(matcher["name"])
        func = getattr(EspressoCriteria, func_name)(matcher["args"], driver=driver, root=root,
                                                    referrer="with_class_name")

        def f(e: XMLElement) -> bool:
            return func(e)

        return f

    @staticmethod
    def with_content_description(arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement):
        text = arg[0]["content"]

        def f(e: XMLElement) -> bool:
            cd = e.get("content-desc")

            if cd is None:
                return False

            return e.get("content-desc") == text

        return f

    @staticmethod
    def with_hint(arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement):
        text = arg[0]["content"]

        def f(e: XMLElement) -> bool:
            hint = e.get("text")

            if hint is None:
                return False

            return hint == text

        return f

    @staticmethod
    def with_id(arg: List[CriteriaArgument], driver: WebDriver, root: XMLElement):
        id_text = arg[0]["content"]

        def f(e: XMLElement) -> bool:
            rid = e.get("resource-id")

            if rid is None:
                return False

            current_pkg = driver.current_package
            id_format = id_text.split(".")[-1]
            return rid == f"{current_pkg}:id/{id_format}" or rid == f"android:id/{id_format}"

        return f

    @staticmethod
    def with_parent(arg: List[CriteriaArgument | NestedCriteria], driver: WebDriver, root: XMLElement):
        parent_criteria = arg[0]

        func_name = camel_to_snake(parent_criteria["name"])
        func = getattr(EspressoCriteria, func_name)(parent_criteria["args"], driver=driver, root=root)

        def f(e: XMLElement) -> bool:
            if e.get_parent() is None:
                return False

            return func(e.get_parent())

        return f

    @staticmethod
    def with_text(arg: List[CriteriaArgument | NestedCriteria], driver: WebDriver, root: XMLElement):
        if "name" in arg[0]:
            func_name = arg[0]["name"]
            if func_name == "containsString":
                text = arg[0]["args"][0]["content"]

                def f(e: XMLElement) -> bool:
                    return text in e.get("text")

                return f
            elif func_name == "is":
                text = arg[0]["args"][0]["content"]

                def f(e: XMLElement) -> bool:
                    return e.get("text") == text

                return f

        text = arg[0]["content"]

        def f(e: XMLElement) -> bool:
            return e.get("text") == text

        return f
