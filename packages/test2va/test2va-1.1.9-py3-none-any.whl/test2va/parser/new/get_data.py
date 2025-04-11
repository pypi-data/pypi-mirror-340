from typing import List, Literal, Optional, Union

from test2va.util import filter_list

from test2va.const import NSURL

from test2va.parser.structs.XMLElement import XMLElement
from test2va.parser.types.NewGrammar import ParseData, MatcherComponent, MatcherData, ActionData

SUPPORTED_MATCH_TYPES = ["allOf", "anyOf"]

"""
Assumptions:
- Actions come directly after matchers
- Assertions are the last thing to happen in the method.
"""

matcher_map = []
special_action_map = []


def parse_data_by_annotation(root: XMLElement, anno: str, data_arr: List[MatcherData], asserts=None):
    """Extracts test steps (matchers, actions, assertions) based on test annotations.

    Args:
        root (XMLElement): Root XML element representing the test case.
        anno (str): Annotation to filter for (`Before`, `Test`, or `After`).
        data_arr (List[MatcherData]): List to store extracted matcher data.
        asserts (Optional[List[MatcherData]]): List to store extracted assertions if applicable.
    """
    matcher_map.clear()
    special_action_map.clear()
    # Find the first descendant annotation tag with a child name tag with content "Test"
    annotations = root.find_descendants(lambda e: e.tag == f"{{{NSURL}}}annotation")

    for annotation in annotations:
        name = annotation.find_first_child(lambda e: e.tag == f"{{{NSURL}}}name")

        if name is not None and name.text == anno:
            root = annotation.get_parent()

            calls = find_view_matcher_calls(root)

            g = 0
            for call in calls:
                m_data: MatcherData = {
                    "Action": [],
                    "Components": [],
                    "MatchType": get_match_type(call)
                }

                get_match_data(call, m_data["Components"])

                data_arr.append(m_data)
                matcher_map.append(call.get_df_index())

            if asserts is not None:
                assertion_calls = find_assertion_calls(root)
                a = 0
                # Loop down starting from assertion_calls len - 1
                for i in range(len(assertion_calls) - 1, -1, -1):
                    # We are going to move the matcherdata["components"] len - 1 - a to the assertions
                    asserts.append(data_arr[len(data_arr) - 1 - i])
                    # Then we will replace the "action" key with "assertion" and set it equal to get_assertion_data
                    asserts[a]["Action"] = []
                    get_assertion_data(assertion_calls[a], asserts[a]["Action"])
                    # Also, remove them from the calls list
                    data_arr.pop(len(data_arr) - 1 - i)
                    calls.pop(len(calls) - 1 - i)
                    a += 1

            action_calls = find_action_calls(root)

            for i in range(len(calls)):
                get_action_data(action_calls[i], data_arr[i]["Action"])

            find_special_actions(root)

            for sa in special_action_map:
                found = False
                for i in range(len(matcher_map)):
                    target_matcher = data_arr[i]

                    if i + 1 == len(matcher_map) or sa["df_index"] <= matcher_map[i + 1]:
                        # Essentially if is first action in method
                        if sa["df_index"] < matcher_map[i]:
                            data_arr[i]["Action"].insert(0, sa["data"])
                        else:
                            target_matcher["Action"].append(sa["data"])
                        found = True
                        break

                # Found may be false if the special action is the first action in the method.
                # If we are in the setup or teardown function and this is the case,
                # we will create a dummy matcher data to hold the special action.
                # the components array will have a single isDisplayed dummy info.
                if not found and anno != "Test":
                    data_arr.append({
                        "Action": [sa["data"]],
                        "Components": [{"Name": "isDisplayed", "Args": []}],
                        "MatchType": "allOf"
                    })


def get_parse_data(root: XMLElement) -> List[ParseData]:
    """Parses an XML representation of a test case to extract structured test data.

    This function extracts test setup steps (`@Before`), test execution steps (`@Test`),
    and teardown steps (`@After`), processing view matchers, actions, and assertions.

    Args:
        root (XMLElement): Root XML element representing the test case.

    Returns:
        List[ParseData]: A list of parsed test data containing test steps and assertions.
    """
    index_map = {}
    assign_df_index(root)
    name = get_test_func_name(root)

    data = {
        "Assertions": [],
        "After": [],
        "Before": [],
        "Matchers": [],
        "Name": name,
    }

    parse_data_by_annotation(root, "Before", data["Before"])
    parse_data_by_annotation(root, "Test", data["Matchers"], data["Assertions"])
    parse_data_by_annotation(root, "After", data["After"])

    # We are going to sort the indexes of the matchers so that they are in order based on their index in the map.
    return [data]


def find_special_actions(root: XMLElement):
    """Finds and processes special actions such as `Thread.sleep` and `pressBack` in test cases.

    Args:
        root (XMLElement): Root XML element representing the test case.
    """
    # Thread.sleep
    def sleep_func(e: XMLElement) -> bool:
        if e.tag != f"{{{NSURL}}}call":
            return False

        name = e.find_first_child(lambda e_: e_.tag == f"{{{NSURL}}}name")

        text = ""
        for child in name.get_children():
            if child.text is not None:
                text += child.text

        return text == "Thread.sleep"

    sleep_calls = root.find_descendants_dfs(sleep_func)

    for call in sleep_calls:
        to_append: ActionData = {
            "Name": "sleep",
            "Args": [[call.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}literal").text]]
        }

        special_data = {
            "df_index": call.get_df_index(),
            "data": to_append
        }

        special_action_map.append(special_data)

    # pressBack
    def back_func(e: XMLElement) -> bool:
        if e.tag != f"{{{NSURL}}}call":
            return False

        name = e.find_first_child(lambda e_: e_.tag == f"{{{NSURL}}}name")

        return name.text == "pressBack"

    back_calls = root.find_descendants_dfs(back_func)

    for call in back_calls:
        to_append: ActionData = {
            "Name": "pressBack",
            "Args": []
        }

        special_data = {
            "df_index": call.get_df_index(),
            "data": to_append
        }

        special_action_map.append(special_data)


def assign_df_index(root: XMLElement):
    """Assigns a unique depth-first index to each XML element for ordering.

    Args:
        root (XMLElement): Root XML element.
    """
    df_index = 0
    root.set_df_index(df_index)

    for desc in root.find_descendants_dfs(lambda e: True):
        df_index += 1
        desc.set_df_index(df_index)


def get_test_func_name(root: XMLElement) -> [str, XMLElement]:
    """Extracts the function name of the test method.

    Args:
        root (XMLElement): Root XML element representing the test case.

    Returns:
        str: Name of the test function.
    """
    # Find the first descendant annotation tag with a child name tag with content "Test"
    annotations = root.find_descendants(lambda e: e.tag == f"{{{NSURL}}}annotation")

    for annotation in annotations:
        name = annotation.find_first_child(lambda e: e.tag == f"{{{NSURL}}}name")

        if name is not None and name.text == "Test":
            block = annotation.get_parent()
            containing_func_name = block.find_first_child(lambda e: e.tag == f"{{{NSURL}}}name")
            return containing_func_name.text


def find_action_calls(root: XMLElement) -> List[XMLElement]:
    """Finds all occurrences of `perform()` calls in the test case.

    Args:
        root (XMLElement): Root XML element representing the test case.

    Returns:
        List[XMLElement]: List of XML elements representing `perform()` calls.
    """
    def matching_func(e: XMLElement) -> bool:
        if e.tag != f"{{{NSURL}}}call":
            return False

        name = e.find_first_child(lambda e_: e_.tag == f"{{{NSURL}}}name")

        if name is None:
            return False

        if name.text is not None and name.text == "perform":
            return True

        name_two = name.find_first_child(lambda e_: e_.tag == f"{{{NSURL}}}name" and e_.text == "perform")

        return name_two is not None

    return root.find_descendants_dfs(matching_func)


def find_assertion_calls(root: XMLElement) -> List[XMLElement]:
    """Finds all occurrences of `check()` assertions in the test case.

    Args:
        root (XMLElement): Root XML element representing the test case.

    Returns:
        List[XMLElement]: List of XML elements representing `check()` assertions.
    """
    def matching_func(e: XMLElement) -> bool:
        if e.tag != f"{{{NSURL}}}call":
            return False

        name = e.find_first_child(lambda e_: e_.tag == f"{{{NSURL}}}name")

        if name is None:
            return False

        if name.text is not None and name.text == "check":
            return True

        name_two = name.find_first_child(lambda e_: e_.tag == f"{{{NSURL}}}name" and e_.text == "check")

        return name_two is not None

    return root.find_descendants_dfs(matching_func)


def find_view_matcher_calls(root: XMLElement, ignore_nested=True) -> List[XMLElement]:
    """Finds all occurrences of `onView()` calls in the test case.

    Args:
        root (XMLElement): Root XML element representing the test case.
        ignore_nested (bool): Whether to ignore nested `onView()` calls.

    Returns:
        List[XMLElement]: List of XML elements representing `onView()` calls.
    """
    # Looking for calls with a name child with text "onView"
    def matching_func(e: XMLElement) -> bool:
        if e.tag != f"{{{NSURL}}}call":
            return False

        name = e.find_first_child(lambda e: e.tag == f"{{{NSURL}}}name")

        if name is None:
            return False

        if ignore_nested:
            # If the call has an ancestor call with child name "onView" then ignore it.
            def matching_nested(e_: XMLElement) -> bool:
                if e_.depth() < root.depth():
                    return False

                if e_.tag != f"{{{NSURL}}}call":
                    return False

                nest_name = e_.find_first_child(lambda e__: e__.tag == f"{{{NSURL}}}name")

                if nest_name is None:
                    return False

                if nest_name.text == "onView":
                    return True

                if nest_name.text == "perform":
                    return True

                if nest_name.text == "check":
                    return True

                return False

            if e.is_a_descendant_of(matching_nested):
                return False

        return name.text == "onView"

    return root.find_descendants_dfs(matching_func)


def get_action_data(act_call: XMLElement, arr: Optional[List['ActionData']]):
    """Extracts action data from a call element.

    Args:
        act_call (XMLElement): XML element representing the action call.
        arr (Optional[List[ActionData]]): List to store extracted action data.
    """
    argument_list = act_call.find_first_child(lambda e: e.tag == f"{{{NSURL}}}argument_list")

    if argument_list is None:
        return None

    args = filter(lambda e: e.tag == f"{{{NSURL}}}argument", argument_list.get_children())

    for arg in args:
        arg_name = arg.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}name")

        if arg_name is None:
            continue

        arg_name = arg_name.text

        if arg_name not in parsing_action_map:
            continue

        data: ActionData = {
            "Name": arg_name,
            "Args": []
        }

        args_arg_list = arg.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}argument_list")
        args_args = filter_list(args_arg_list.get_children(), lambda e: e.tag == f"{{{NSURL}}}argument")

        for i in range(len(args_args)):
            func = parsing_action_map[arg_name][i]
            func(args_args[i], data["Args"])

        arr.append(data)


def get_assertion_data(act_call: XMLElement, arr: Optional[List['ActionData']]):
    """Extracts assertion data from a call element.

    Args:
        act_call (XMLElement): XML element representing the assertion call.
        arr (Optional[List[ActionData]]): List to store extracted assertion data.
    """
    argument_list = act_call.find_first_child(lambda e: e.tag == f"{{{NSURL}}}argument_list")

    if argument_list is None:
        return None

    args = filter(lambda e: e.tag == f"{{{NSURL}}}argument", argument_list.get_children())

    for arg in args:
        arg_name = arg.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}name")

        if arg_name is None:
            continue

        arg_name = arg_name.text

        if arg_name not in parsing_assertion_map:
            continue

        data: ActionData = {
            "Name": arg_name,
            "Args": []
        }

        args_arg_list = arg.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}argument_list")
        args_args = filter_list(args_arg_list.get_children(), lambda e: e.tag == f"{{{NSURL}}}argument")

        for i in range(len(args_args)):
            func = parsing_assertion_map[arg_name][i]
            func(args_args[i], data["Args"])

        arr.append(data)


def get_match_data(vm_call: XMLElement, arr: List[MatcherComponent], nested_origin=False):
    """Extracts matcher data from a call element.

    Args:
        vm_call (XMLElement): XML element representing the matcher call.
        arr (List[MatcherComponent]): List to store extracted matcher data.
        nested_origin (bool): Whether the call is a nested matcher call.
    """
    argument_list = vm_call.find_first_child(lambda e: e.tag == f"{{{NSURL}}}argument_list")

    if not nested_origin:
        name = argument_list.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}name")
        if name is not None and name.text in SUPPORTED_MATCH_TYPES:
            argument_list = argument_list.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}argument_list")

    # Get all children arguments
    args = filter(lambda e: e.tag == f"{{{NSURL}}}argument", argument_list.get_children())

    for arg in args:
        arg_name = arg.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}name")

        if arg_name is None:
            continue

        arg_name = arg_name.text

        if arg_name not in parsing_map:
            continue

        data: MatcherComponent = {
            "Name": arg_name,
            "Args": []
        }

        args_arg_list = arg.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}argument_list")
        args_args = filter_list(args_arg_list.get_children(), lambda e: e.tag == f"{{{NSURL}}}argument")

        for i in range(len(args_args)):
            func = parsing_map[arg_name][i]
            func(args_args[i], data["Args"])

        arr.append(data)


def get_match_type(vm_call: XMLElement) -> Literal["allOf", "anyOf"]:
    """Determines the matcher type (`allOf` or `anyOf`).

    Args:
        vm_call (XMLElement): XML element representing a matcher call.

    Returns:
        Literal["allOf", "anyOf"]: Matcher type.
    """
    arg_list = vm_call.find_first_child(lambda e: e.tag == f"{{{NSURL}}}argument_list")

    if arg_list is None:
        return "allOf"

    possibly_match_type_name = arg_list.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}name")

    if possibly_match_type_name is None:
        return "allOf"

    if possibly_match_type_name.text not in SUPPORTED_MATCH_TYPES:
        return "allOf"

    return possibly_match_type_name.text


def action_nested_args(argument_tag: XMLElement,
                       arg_arr: Optional[List[Union[List[str], List['ParseData'], List[ActionData]]]]):
    """Extracts nested action arguments from a call element.

    Args:
        argument_tag (XMLElement): XML element representing the action call.
        arg_arr (Optional[List[Union[List[str], List[ParseData], List[ActionData]]]]): List to store extracted action data.
    """
    nested_call = argument_tag.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}call")

    if nested_call is None:
        return

    name = nested_call.find_first_child(lambda e: e.tag == f"{{{NSURL}}}name")

    if name is None:
        return

    action_name = name.text

    if action_name not in parsing_action_map:
        print(f"Action {action_name} not found in parsing_action_map")
        return

    data: ActionData = {
        "Name": action_name,
        "Args": []
    }

    args_arg_list = nested_call.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}argument_list")
    args_args = filter_list(args_arg_list.get_children(), lambda e: e.tag == f"{{{NSURL}}}argument")

    for i in range(len(args_args)):
        func = parsing_action_map[action_name][i]
        func(args_args[i], data["Args"])

    arg_arr.append([data])


def assertion_nested_args(argument_tag: XMLElement,
                          arg_arr: Optional[List[Union[List[str], List['ParseData'], List[ActionData]]]]):
    """Extracts nested assertion arguments from a call element.

    Args:
        argument_tag (XMLElement): XML element representing the assertion call.
        arg_arr (Optional[List[Union[List[str], List[ParseData], List[ActionData]]]]): List to store extracted assertion data.
    """
    nested_call = argument_tag.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}call")

    if nested_call is None:
        return

    name = nested_call.find_first_child(lambda e: e.tag == f"{{{NSURL}}}name")

    if name is None:
        return

    action_name = name.text

    if action_name not in parsing_assertion_map:
        print(f"Action {action_name} not found in parsing_action_map")
        return

    data: ActionData = {
        "Name": action_name,
        "Args": []
    }

    args_arg_list = nested_call.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}argument_list")
    args_args = filter_list(args_arg_list.get_children(), lambda e: e.tag == f"{{{NSURL}}}argument")

    for i in range(len(args_args)):
        func = parsing_assertion_map[action_name][i]
        func(args_args[i], data["Args"])

    arg_arr.append([data])


def action_click_special(argument_tag: XMLElement,
                         arg_arr: Optional[List[Union[List[str], List['ParseData'], List['ActionData']]]]):
    """Handles special action click arguments.

    Args:
        argument_tag (XMLElement): XML element representing the action call.
        arg_arr (Optional[List[Union[List[str], List[ParseData], List[ActionData]]]]): List to store extracted action data.
    """
    literal = argument_tag.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}literal")

    if literal is not None:
        arg_arr.append([literal.text])
        return

    # We must be dealing with a nested action

    nested_call = argument_tag.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}call")

    if nested_call is None:
        return

    name = nested_call.find_first_child(lambda e: e.tag == f"{{{NSURL}}}name")

    if name is None:
        return

    action_name = name.text

    if action_name not in parsing_action_map:
        return

    data: ActionData = {
        "Name": action_name,
        "Args": []
    }

    args_arg_list = nested_call.find_first_descendant(lambda e: e.tag == f"{{{NSURL}}}argument_list")
    args_args = filter_list(args_arg_list.get_children(), lambda e: e.tag == f"{{{NSURL}}}argument")

    for i in range(len(args_args)):
        func = parsing_action_map[action_name][i]
        func(args_args[i], data["Args"])

    arg_arr.append([data])


# This should cover literals, ids.in.this.form, and matcher.s
def matcher_literal_args(argument_tag: XMLElement, arg_arr: Optional[List[Union[List[str], List['ParseData']]]]):
    """Extracts literal arguments from a call element.

    Args:
        argument_tag (XMLElement): XML element representing the call.
        arg_arr (Optional[List[Union[List[str], List[ParseData]]]]): List to store extracted literal data.
    """
    argument_list = argument_tag.find_first_child(lambda e: e.tag == f"{{{NSURL}}}argument_list")

    if argument_list is None:
        argument_list = argument_tag

    # Do a depth first search to get all text from elements if it exists
    desc = argument_list.find_descendants(lambda e: e.text is not None and e.text != '')

    arr = []

    for d in desc:
        arr.append(d.text)

    arg_arr.append(arr)


def matcher_nested_args(argument_tag: XMLElement, arg_arr: Optional[List[Union[List[str], List['ParseData']]]],
                        nested_origin=False):
    """Extracts nested matcher arguments from a call element.

    Args:
        argument_tag (XMLElement): XML element representing the matcher call.
        arg_arr (Optional[List[Union[List[str], List[ParseData]]]]): List to store extracted matcher data.
        nested_origin (bool): Whether the call is a nested matcher call.
    """
    nested_calls = find_view_matcher_calls(argument_tag)

    if len(nested_calls) == 0:
        if nested_origin:
            nested_calls = [argument_tag.get_parent().get_parent()]
        else:
            return

    nested_call = nested_calls[0]

    arg: Optional[ParseData] = {"Matchers": []}

    data: MatcherData = {
        "Action": None,
        "Components": [],
        "MatchType": get_match_type(nested_call)
    }

    get_match_data(nested_call, data["Components"], nested_origin)

    arg["Matchers"].append(data)

    arg_arr.append([arg])


def matcher_nested_arg_for_map(argument_tag: XMLElement, arg_arr: Optional[List[Union[List[str], List['ParseData']]]]):
    matcher_nested_args(argument_tag, arg_arr, True)


def matcher_no_args(argument_tag: XMLElement, arg_arr: Optional[List[Union[List[str], List['ParseData']]]]):
    arg_arr = None


parsing_map = {
    "childAtPosition": [matcher_nested_arg_for_map, matcher_literal_args],
    "doesNotHaveFocus": [matcher_no_args],
    "hasBackground": [matcher_literal_args],
    "hasChildCount": [matcher_literal_args],
    "hasContentDescription": [matcher_no_args],
    "hasDescendant": [matcher_nested_arg_for_map],
    "hasErrorText": [matcher_literal_args],
    "hasFocus": [matcher_no_args],
    "hasImeAction": [matcher_literal_args],
    "hasLinks": [matcher_no_args],
    "hasMinimumChildCount": [matcher_literal_args],
    "hasSibling": [matcher_nested_arg_for_map],
    "hasTextColor": [matcher_literal_args],
    "isAssignableFrom": [matcher_no_args],
    "isChecked": [matcher_no_args],
    "isClickable": [matcher_no_args],
    "isCompletelyDisplayed": [matcher_no_args],
    "isDescendantOfA": [matcher_nested_arg_for_map],
    "isDisplayed": [matcher_no_args],
    "isDisplayingAtLeast": [matcher_literal_args],
    "isEnabled": [matcher_no_args],
    "isFocusable": [matcher_no_args],
    "isFocused": [matcher_no_args],
    "isJavascriptEnabled": [matcher_no_args],
    "isNotChecked": [matcher_no_args],
    "isNotClickable": [matcher_no_args],
    "isNotEnabled": [matcher_no_args],
    "isNotFocusable": [matcher_no_args],
    "isNotFocused": [matcher_no_args],
    "isNotSelected": [matcher_no_args],
    "isRoot": [matcher_no_args],
    "isSelected": [matcher_no_args],
    "supportsInputMethods": [matcher_no_args],
    "withAlpha": [matcher_literal_args],
    "withChild": [matcher_nested_arg_for_map],
    "withClassName": [matcher_literal_args],
    "withContentDescription": [matcher_literal_args],
    "withEffectiveVisibility": [matcher_no_args],
    "withHint": [matcher_literal_args],
    "withId": [matcher_literal_args],
    "withInputType": [matcher_literal_args],
    "withParent": [matcher_nested_arg_for_map],
    "withParentIndex": [matcher_literal_args],
    "withResourceName": [matcher_literal_args],
    "withSpinnerText": [matcher_literal_args],
    "withSubstring": [matcher_literal_args],
    "withTagKey": [matcher_literal_args],
    "withTagValue": [matcher_literal_args],
    "withText": [matcher_literal_args]
}

parsing_action_map = {
    "actionOnItemAtPosition": [matcher_literal_args, action_nested_args],
    "clearText": [matcher_no_args],
    "click": [action_click_special, matcher_literal_args],
    "closeSoftKeyboard": [matcher_no_args],
    "doubleClick": [matcher_no_args],
    "longClick": [matcher_no_args],
    "isNotChecked": [matcher_no_args],
    "openLinkWithText": [matcher_literal_args],
    "openLinkWithUri": [matcher_literal_args],
    "pressBack": [matcher_no_args],
    "pressBackUnconditionally": [matcher_no_args],
    "pressImeActionButton": [matcher_no_args],
    "pressKey": [matcher_literal_args],
    "pressMenuKey": [matcher_no_args],
    "repeatedlyUntil": [action_nested_args, matcher_nested_arg_for_map, matcher_literal_args],
    "replaceText": [matcher_literal_args],
    "scrollTo": [matcher_nested_arg_for_map],
    "slowSwipeLeft": [matcher_no_args],
    "swipeDown": [matcher_no_args],
    "swipeLeft": [matcher_no_args],
    "swipeRight": [matcher_no_args],
    "swipeUp": [matcher_no_args],
    "typeText": [matcher_literal_args],
    "typeTextIntoFocusedView": [matcher_literal_args]
}

parsing_assertion_map = {
    # TODO: "allOf": [matcher_literal_args] this has variable sized arguments
    # TODO: Make a case for all of where it checks all of the allOf arguments
    "doesNotExist": [matcher_no_args],
    "matches": [assertion_nested_args],
    "isChecked": [matcher_no_args],
    "isClickable": [matcher_no_args],
    "isDisplayed": [matcher_no_args],
    "isEnabled": [matcher_no_args],
    "isNotChecked": [matcher_no_args],
    "isNotClickable": [matcher_no_args],
    "not": [assertion_nested_args],
    "withSubstring": [matcher_literal_args],
    "withText": [matcher_literal_args]
}
