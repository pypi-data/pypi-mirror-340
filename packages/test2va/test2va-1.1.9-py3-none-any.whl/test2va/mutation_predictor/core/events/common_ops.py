import json
from typing import Tuple, List

from pydantic import BaseModel

from test2va.mutation_predictor.core.basic_test.XMLNode import XMLNode
from test2va.mutation_predictor.core.basic_test.TestAssertion import TestAssertion
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent
from test2va.mutation_predictor.core.basic_test.TestTypes import EventType, ElementMatchingType
from test2va.mutation_predictor.util.gpt_util import get_response_from_gpt
from test2va.mutation_predictor.util.util import read_file_to_string, list_to_str


class ClickEventTypeGPT(BaseModel):
    is_click: bool


class NodeWithDescendantGPT(BaseModel):
    node_with_descendant: str


class NonClickEventTypeGPT(BaseModel):
    is_typed_in: bool
    is_scroll: bool
    is_swipe: bool
    none_of_them: bool


class MatchType1GPT(BaseModel):
    node: str
    class_attribute_value: str
    same_depth_nodes_with_same_class: list[str]


class MatchType2GPT(BaseModel):
    node_without_ancestors: str
    node_with_ancestors: str
    class_attribute_value: str
    same_depth_nodes_has_same_class_with_ancestors: list[str]


class MatchType3GPT(BaseModel):
    node_without_descendants: str
    node_with_descendants: str
    class_attribute_value: str
    same_depth_nodes_has_same_class_with_descendants: list[str]


class MatchType4GPT(BaseModel):
    node: str


class XpathGPT(BaseModel):
    class_name: str
    index: int
    text: str
    resource_id: str
    checked: str
    package: str
    content_desc: str
    bounds: str
    xpath: str


class OriginNodeGPT(BaseModel):
    node: str


class SiblingOriginalNodeGPT(BaseModel):
    node: str


class MatchingTypeGPT(BaseModel):
    use_with_parent: bool
    use_has_descendant: bool
    use_none_of_them: bool
    use_both_of_them: bool


class XpathVerifyGPT(BaseModel):
    number_of_matched_nodes: int
    only_one_node_matched: bool


class CountNodeNumbersInXMLGPT(BaseModel):
    number_of_nodes: int


def identify_event_type(event) -> EventType:
    """
    Make decision by measure the non-click type and click type
    :param event:
    :return: EventType
    """
    # get non-click type decision
    gpt_response: str = event_non_click_type_request(event)
    non_click_type_decision = event_non_click_type_request_handler(gpt_response)

    # get click type decision
    gpt_response: str = event_click_type_request(event)
    click_type_decision = event_click_type_request_handler(gpt_response)

    # made decision:
    if non_click_type_decision.get("is_typed_in"):
        return EventType.Type2
    elif non_click_type_decision.get("is_swipe"):
        return EventType.Type4
    elif non_click_type_decision.get("is_scroll"):
        if click_type_decision.get("is_click"):
            return EventType.Type5
        else:
            return EventType.Type3
    elif non_click_type_decision.get("none_of_them"):
        if click_type_decision.get("is_click"):
            return EventType.Type1
        else:
            raise ValueError(f"The event type cannot be determined: {event.get_statement()}")
    else:
        raise ValueError(f"The event type cannot be determined: {event.get_statement()}")


def event_non_click_type_request(event: TestEvent) -> str:
    """
    Send request to GPT to get suggested non-click event type.
    :param event: TestEvent object

    :return: event type suggestion from gpt
    """

    user_prompt \
        = ("In the below java test statement using Android Espresso, is it "
           "a typed-in event(using typeText(), replaceText(), etc.), "
           "a scrolling event(using scroll(), scrollTo(), actionOnItemAtPosition(), etc.), "
           "or a swipe event (using swipeLeft(), swipeRight(), etc.)? "
           "Or none of them? "
           "No explanation.\n"
           "%s\n" % event.get_statement())

    return get_response_from_gpt(user_prompt, NonClickEventTypeGPT)


def event_non_click_type_request_handler(gpt_response) -> json:
    """
    Converts a gpt response to a json object of decisions

    :param gpt_response: gpt response in json str
    :raise ValueError: gpt response is not what we expected
    :return: The corresponding AssertionType
    """

    # step 1. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 2. get decision
    return response_json


def event_click_type_request(event: TestEvent) -> str:
    """
    Send request to GPT to get suggested event type.
    :param event: TestEvent object

    :return: event type suggestion from gpt
    """

    user_prompt \
        = ("In the below java test statement using Android Espresso, is it "
           "a click event or not? "
           "No explanation.\n"
           "%s\n" % event.get_statement())

    return get_response_from_gpt(user_prompt, ClickEventTypeGPT)


def event_click_type_request_handler(gpt_response) -> json:
    """
    Converts a gpt response to a json object of decisions

    :param gpt_response: gpt response in json str
    :raise ValueError: gpt response is not what we expected
    :return: The corresponding AssertionType
    """

    # step 1. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 2. get decision
    return response_json


def event_type_request_handler(gpt_response) -> EventType:
    """
    Converts a gpt response to the corresponding EventType.

    :param gpt_response: gpt response in json str
    :raise ValueError: gpt response is not what we expected
    :return: The corresponding AssertionType
    """

    # step 1. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 2. get type
    if response_json.get("is_click_only"):
        return EventType.Type1
    elif response_json.get("is_typed_in"):
        return EventType.Type2
    elif response_json.get("is_scroll_only"):
        return EventType.Type3
    elif response_json.get("is_swipe"):
        return EventType.Type4
    elif response_json.get("is_scroll_and_click"):
        return EventType.Type5
    elif response_json.get("none_of_them"):
        return EventType.Type6
    else:
        raise ValueError(f"The response cannot decide the type: {gpt_response}")


def collect_event_origin_node(event_statement: str,
                              full_xml_context_path: str) -> str:
    """
    collect the node of original event statement

    :param event_statement:
    :param full_xml_context_path:
    :return:
    """
    gpt_response: str = collect_event_origin_node_by_statement_request(event_statement, full_xml_context_path)
    return collect_event_origin_node_by_statement_request_handler(gpt_response)


def collect_event_origin_node_by_statement_request(event_statement, full_xml_context_path):
    # read the xml tree content
    xml_context = read_file_to_string(full_xml_context_path)

    # prepare user prompt
    user_prompt = \
        ("Which node in the below xml tree does the statement: \"%s\" represent? "
         "%s" % (event_statement, xml_context))

    return get_response_from_gpt(user_prompt, OriginNodeGPT)


def collect_event_origin_node_by_statement_request_handler(gpt_response) -> str:
    # step 1. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 2. get results
    original_node = response_json.get("node")

    return original_node


def identify_matching_types_request(statement):
    # prepare user prompt
    user_prompt = \
        ("In the statement: \"%s\","
         "Does it use the withParent() method? "
         "Does it use the hasDescendant() method? "
         "Does it use both of them? Or does it use none of them?"
         % statement)

    return get_response_from_gpt(user_prompt, MatchingTypeGPT)


def identify_matching_types_request_handler(gpt_response):
    # step 1. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # decide the matching type
    if response_json.get("use_none_of_them"):
        return ElementMatchingType.Type1
    elif response_json.get("use_both_of_them"):
        return ElementMatchingType.Type4
    elif response_json.get("use_with_parent") and not response_json.get("use_has_descendant"):
        return ElementMatchingType.Type2
    elif not response_json.get("use_with_parent") and response_json.get("use_has_descendant"):
        return ElementMatchingType.Type3
    else:
        raise ValueError(f"The response cannot decide the type: {gpt_response}")


def identify_matching_types(statement) -> ElementMatchingType:
    gpt_response = identify_matching_types_request(statement)
    return identify_matching_types_request_handler(gpt_response)


def collect_event_sibling_nodes(event_statement: str,
                                full_xml_context_path: str) -> Tuple[XMLNode, list[XMLNode]]:
    """
    Collect the potential mutable sibling nodes of the original node.
    Note that sibling node should have different context based on the matcher used in statement:
    hasParent? hasDescendant? None of them?

    :param event_statement:
    :param full_xml_context_path:
    :return:
    """
    sibling_type: ElementMatchingType = identify_matching_types(event_statement)

    if sibling_type is ElementMatchingType.Type1:  # node itself
        return collect_event_sibling_nodes_type1(event_statement, full_xml_context_path)
    elif sibling_type is ElementMatchingType.Type2:  # node with ancestors
        return collect_event_sibling_nodes_type2(event_statement, full_xml_context_path)
    elif sibling_type is ElementMatchingType.Type3:  # node and its Descendant
        return collect_event_sibling_nodes_type3(event_statement, full_xml_context_path)
    elif sibling_type is ElementMatchingType.Type4:  # both
        return collect_event_sibling_nodes_type4(event_statement, full_xml_context_path)
    else:
        raise ValueError(f"The sibling type is never seen {event_statement}")


def collect_event_sibling_nodes_type1(event_statement, full_xml_context_path) -> Tuple[XMLNode, list[XMLNode]]:
    """
    Collect the XML node and its siblings without the context.

    :param event_statement:
    :param full_xml_context_path:
    :return:
    """
    # read the xml tree content
    xml_context = read_file_to_string(full_xml_context_path)

    # step 1. prepare user prompt
    user_prompt = \
        ("Which node in the below xml tree does the statement: \"%s\" represent? "
         "What is the value of this node's class attribute? "
         "What are all the rest nodes with same depth of this node and have the same value of class attribute? "
         "%s" % (event_statement, xml_context))

    # step 2. send the request
    gpt_response = get_response_from_gpt(user_prompt, MatchType1GPT)

    # step 3. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 4. handle results
    original_node = XMLNode(response_json.get("node"), ElementMatchingType.Type1)

    sibling_nodes = []
    for node_value in response_json.get("same_depth_nodes_with_same_class"):
        xml_node = XMLNode(node_value, ElementMatchingType.Type1)
        sibling_nodes.append(xml_node)

    return original_node, sibling_nodes


def collect_event_sibling_nodes_type2(event_statement, full_xml_context_path) -> Tuple[XMLNode, list[XMLNode]]:
    """
    collect the event sibling nodes with matching type of 2, including parent matching

    :param event_statement:
    :param full_xml_context_path:
    :return:
    """
    # read the xml tree content
    xml_context = read_file_to_string(full_xml_context_path)

    # step 1. prepare user prompt
    user_prompt = \
        ("Which node in the below xml tree does the statement: \"%s\" represent? "
         "Additionally, please also output the found node with all its ancestors in the tree."
         "What is the value of this node's class attribute? "
         "What are all the rest nodes with same depth of this node and have the same value of class attribute? "
         "Please also output all these nodes with their ancestors.\n "
         "%s" % (event_statement, xml_context))

    # step 2. send the request
    gpt_response = get_response_from_gpt(user_prompt, MatchType2GPT)

    # step 3. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 4. handle results
    original_node = XMLNode(response_json.get("node_without_ancestors"), ElementMatchingType.Type2,
                            response_json.get("node_with_ancestors"))

    sibling_nodes = []
    for node_value_with_context in response_json.get("same_depth_nodes_has_same_class_with_ancestors"):
        node_value: str = get_original_node_value_from_context(ElementMatchingType.Type2, node_value_with_context)
        xml_node = XMLNode(node_value, ElementMatchingType.Type2, node_value_with_context)
        sibling_nodes.append(xml_node)

    return original_node, sibling_nodes


def collect_event_sibling_nodes_type3(event_statement, full_xml_context_path) -> Tuple[XMLNode, list[XMLNode]]:
    """
    collect the event sibling nodes with matching type of 3, including descendants matching
    :param event_statement:
    :param full_xml_context_path:
    :return:
    """
    # read the xml tree content
    xml_context = read_file_to_string(full_xml_context_path)

    # prepare user prompt
    user_prompt = \
        ("Which node in the below xml tree does the statement: \"%s\" represent? "
         "Please output the node with all its descendants in the tree."
         "What is the value of this node's class attribute? "
         "What are all the rest nodes with same depth of this node and have the same value of class attribute? "
         "Please output all these nodes with their descendants.\n "
         "%s" % (event_statement, xml_context))

    # step 2. send the request
    gpt_response = get_response_from_gpt(user_prompt, MatchType3GPT)

    # step 3. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 4. handle results
    original_node = XMLNode(response_json.get("node_without_descendants"), ElementMatchingType.Type3,
                            response_json.get("node_with_descendants"))

    sibling_nodes = []
    for node_value_with_context in response_json.get("same_depth_nodes_has_same_class_with_descendants"):
        node_value: str = get_original_node_value_from_context(ElementMatchingType.Type3, node_value_with_context)
        xml_node = XMLNode(node_value, ElementMatchingType.Type3, node_value_with_context)
        sibling_nodes.append(xml_node)

    return original_node, sibling_nodes


def collect_event_sibling_nodes_type4(event_statement, full_xml_context_path) -> Tuple[XMLNode, list[XMLNode]]:
    """
    In type4, the whole tree will be the sibling nodes.

    :param event_statement:
    :param full_xml_context_path:
    :return:
    """
    # read the xml tree content
    xml_context = read_file_to_string(full_xml_context_path)

    # step1. prepare user prompt
    user_prompt = \
        ("Which node in the below xml tree does the statement: \"%s\" represent? "
         "%s" % (event_statement, xml_context))

    # step2. send request
    gpt_response = get_response_from_gpt(user_prompt, MatchType4GPT)

    # step3. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step4. handle results
    # In type4, the sibling nodes should be the entire xml tree.
    # So we put the xml tree as node's context, and return an empty sibling node list, since they are not
    # reliable.
    original_node = XMLNode(response_json.get("node"), ElementMatchingType.Type4, xml_context)

    return original_node, []


# def build_xpath_from_single_node(node: str) -> str:
#     """
#     build the xpath from the provided node, if empty, return empty string
#     :param node:
#     :return:
#     """
#     response: str = get_xpath_from_node_request(node)
#     xpath: str = get_xpath_from_node_request_handler(response)
#
#     if xpath:
#         xpath = xpath.replace("][", "")  # remove ][ to put all attributes in one [].
#         return xpath
#     else:
#         return ""


def get_original_node_value_from_context(node_type: ElementMatchingType, node_with_context: str) -> str:
    """
    get the original node from node context
    :param element:
    :return:
    """

    user_prompt = ""
    if node_type == ElementMatchingType.Type2:
        user_prompt = \
            ("Below is an xml tree, what is the root node?\n"
             "%s" % node_with_context)
    elif node_type == ElementMatchingType.Type3:
        user_prompt = \
            ("Below is an xml tree, what is the leaf node?\n"
             "%s" % node_with_context)

    response = get_response_from_gpt(user_prompt, SiblingOriginalNodeGPT)
    response_json = json.loads(response.strip())

    return response_json.get("node")


def build_xpath_from_xml_node(xml_node: XMLNode, full_xml_context_path: str) -> str:
    """
    build the xpath from the provided node.
    if failed in verify, means the xpath will lead to multiple node, and then add the bounds.
    :param full_xml_context_path:
    :param xml_node:
    :return:
    """

    # 1. read the xml tree content
    xml_context = read_file_to_string(full_xml_context_path)

    # 2. get node value and build the xpath
    node: str = xml_node.get_node_value()
    xpath: str = get_xpath_from_node_without_bounds(node)

    # if xpath is empty, return empty string
    if not xpath:
        return ""

    # xpath generated, verify the xpath
    not_duplicated = verify_xpath_not_duplicated(xpath, xml_context)

    if not_duplicated:
        return xpath
    else:  # if failed, including the bounds in xpath
        return get_xpath_from_node_with_bounds(node)


def verify_xpath_not_duplicated(xpath: str, xml_context: str):
    user_prompt = \
        ("Below is an xml tree, how many nodes does this xpath \"%s\" match to? "
         "Is there only one node that matched?\n"
         "%s" % (xpath, xml_context))

    response: str = get_response_from_gpt(user_prompt, XpathVerifyGPT)
    response_json = json.loads(response.strip())

    if response_json.get("number_of_matched_nodes") == 1 and response_json.get("only_one_node_matched"):
        return True
    else:
        return False


def get_xpath_from_node_without_bounds(node: str):

    # 1. prepare prompt
    user_prompt = \
        ("Generate the xpath for node: \"%s\". "
         "Including the attributes of index, text, resource-id, class, checked, package, content-desc, enabled "
         "skip if they are none or empty. "
         "Follow the format of \"//class[attribute='value']\", "
         "please put all attributes and their values together in one []. "
         "Connecting attributes using keyword 'and' and using single quote for attribute values. "
         "" % node)

    # 2. send request
    response: str = get_response_from_gpt(user_prompt, XpathGPT)

    # 3. get response
    response_json = json.loads(response.strip())

    # 4. get result
    return response_json.get("xpath") # .replace("][", "")


def get_xpath_from_node_with_bounds(node: str):
    # 1. prepare prompt
    user_prompt = \
        ("Generate the xpath for node: \"%s\". "
         "Including the attributes of index, text, resource-id, class, checked, package, content-desc, "
         "enabled, and bounds. "
         "Skip the attributes if they are none or empty. "
         "Follow the format of \"//class[attribute='value']\", "
         "please put all attributes and their values together in one []. "
         "Connecting attributes using keyword 'and' and using single quote for attribute values. "
         "" % node)

    # 2. send request
    response: str = get_response_from_gpt(user_prompt, XpathGPT)

    # 3. get response
    response_json = json.loads(response.strip())

    # 4. get result
    return response_json.get("xpath") #.replace("][", "")


def get_xpath_from_node(node: str):
    # 1. prepare prompt
    user_prompt = \
        ("Generate the xpath for node: \"%s\". "
         "Including the attributes of index, text, resource-id, class, checked, package, content-desc, "
         "enabled, and bounds. "
         "Skip the attributes if they are none or empty. "
         "Follow the format of \"//class[attribute='value']\", "
         "please put all attributes and their values together in one []. "
         "Connecting attributes using keyword 'and' and using single quote for attribute values. "
         "" % node)

    # 2. send request
    response: str = get_response_from_gpt(user_prompt, XpathGPT)

    # 3. get response
    response_json = json.loads(response.strip())

    # 4. get result
    return response_json.get("xpath") #.replace("][", "")


def build_xpath_from_statement(statement, full_xml_context_path):
    # 1. read the xml tree content
    xml_context = read_file_to_string(full_xml_context_path)

    # 2. prepare prompt
    user_prompt = \
        ("The statement \"%s\" is related to one node on this xml tree."
         "Please generate the xpath for this node. "
         "Including the attributes of index, text, resource-id, class, checked, package, content-desc, "
         "enabled, and bounds. "
         "Skip the attributes if they are none or empty. "
         "Follow the format of \"//class[attribute='value']\", "
         "please put all attributes and their values together in one []. "
         "Connecting attributes using keyword 'and' and using single quote for attribute values. \n"
         "xml tree:\n"
         "%s" % (statement, xml_context))

    # 3. send request
    response: str = get_response_from_gpt(user_prompt, XpathGPT)

    # 4. get response
    response_json = json.loads(response.strip())

    # 5. get result
    return response_json.get("xpath") #.replace("][", "")


def get_related_assertion(event: TestEvent, assertions: list[TestAssertion]) -> TestAssertion | None:
    # event should only have one related assertion.
    assertion_num = len(event.get_related_assertion_indices())

    if assertion_num == 1:
        return assertions[event.get_related_assertion_indices()[0]]
    elif assertion_num == 0:  # no related assertion
        return None
    else:
        raise ValueError(f"The event has more than one related assertions: {event.get_statement()}")


def build_events_str_list(events: list[TestEvent]) -> list[str]:
    """
    Build a list of TestEvent as a list of strings
    :param events: a list of TestEvent objects
    :return:
    """
    # prepare event list as string
    events_str: list[str] = []
    for event in events:
        events_str.append(event.get_statement())

    return events_str


def build_mutation_report(events: list[TestEvent]) -> dict:
    event_report: dict = {}

    for event in events:
        # step 1. prepare the mutant_events_report
        mutant_events_report = []  # a list of mutant event objs

        if event.get_is_mutable():
            mutant_events = event.get_mutant_events()
            for mutant_event in mutant_events:
                mutant_json = {"origin_event_index": event.get_index(),
                               "statement": mutant_event.get_statement(),
                               "xpath": mutant_event.get_xpath(),
                               "assertion_statement": mutant_event.get_assertion_statement_pairs()}
                mutant_events_report.append(mutant_json)

        # step 2. build json object of current event
        event_json = {"is_mutable": event.get_is_mutable(),
                      "statement": event.get_statement(),
                      "xpath": event.get_xpath(),
                      "mutant_events": mutant_events_report,
                      "test_method_name": event.get_test_method_name(),
                      "mutant_candidates_before": event.get_mutant_candidates_before(),
                      "mutant_candidates_after": event.get_mutant_candidates_after()}

        # step 3. add event json object to final event report
        event_report[event.get_index()] = event_json

    return event_report


def build_test_code_segment(target_event: TestEvent, events: list[TestEvent], assertions: list[TestAssertion]) -> str:
    """
    Given original list of event and list of assertion, build the test code segment for the target event.

    :param target_event:
    :param events:
    :param assertions:
    :return: test code segment as string
    """

    # prepare the event code
    events_str: list[str] = build_events_str_list(events)
    event_test_code: str = list_to_str(events_str)

    # prepare the assertion code
    assertion = get_related_assertion(target_event, assertions)
    if assertions:
        assertion_test_code: str = assertion.get_statement()
    else:
        assertion_test_code: str = ""

    test_code = f"{event_test_code}\n{assertion_test_code}"

    return test_code


def build_event_code_segment(events: list[TestEvent]) -> str:
    """
    Given original list of event, build the event code segment without assertion

    :param events:
    :return: test code segment as string
    """

    # prepare the event code
    events_str: list[str] = build_events_str_list(events)
    event_test_code: str = list_to_str(events_str)

    return event_test_code


def collect_descendant_of_node_request(node, xml_context):
    user_prompt = \
        ("The node \"%s\" comes from the below xml tree. \n"
         "Please output this node with all its descendant. \n"
         "%s" % (node, xml_context))

    return get_response_from_gpt(user_prompt, NodeWithDescendantGPT)


def collect_descendant_of_node_request_handler(response):
    # step 1. convert the response string to json object
    response_json = json.loads(response.strip())

    # step 2. get results
    return response_json.get("node_with_descendant")


def count_number_of_nodes_in_xml_content(full_xml_context_path: str):

    user_prompt = \
        ("How many nodes are there in below Android view hierarchy xml tree? \n"
         "%s"
         % (read_file_to_string(full_xml_context_path)))

    gpt_response = get_response_from_gpt(user_prompt, CountNodeNumbersInXMLGPT)

    response_json = json.loads(gpt_response.strip())

    return response_json.get("number_of_nodes")


def collect_descendant_of_node(node, xml_context) -> str:
    """
    Return the node and its descendant from the page source.
    :param node:
    :param xml_context:
    :return:
    """
    gpt_response: str = collect_descendant_of_node_request(node, xml_context)
    return collect_descendant_of_node_request_handler(gpt_response)


def is_identical_event(mutant_statement: str, event_statement: str):
    """
    Two events are identical when the statement are the same.
    :param mutant_statement:
    :param event_statement:
    :return:
    """
    return mutant_statement.casefold() == event_statement.casefold()