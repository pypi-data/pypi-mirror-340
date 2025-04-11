import json
import os
from typing import Tuple, List

from pydantic import BaseModel

from test2va.mutation_predictor.core.basic_test.MutantEvent import MutantEvent
from test2va.mutation_predictor.core.basic_test.TestAssertion import TestAssertion
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent
from test2va.mutation_predictor.core.basic_test.TestTypes import ScrollType
from test2va.mutation_predictor.core.events.common_ops import get_xpath_from_node, \
    count_number_of_nodes_in_xml_content, is_identical_event
from test2va.mutation_predictor.util.gpt_util import get_response_from_gpt
from test2va.mutation_predictor.util.util import read_file_to_string


class ScrollTypeGPT(BaseModel):
    is_recycle_view: bool
    recycle_view_id: str
    invoke_scroll_to: bool
    scroll_to_has_argument: bool
    argument: str


# class ScrollNodeType1GPT(BaseModel):
#     node: str
#     class_attribute_value: str
#     same_depth_nodes_with_same_class: list[str]
#
#
# class ScrollNodeType2GPT(BaseModel):
#     node_with_descendant: str
#     node_without_descendant: str
#     class_attribute_value: str
#     same_depth_nodes_with_descendant: list[str]
#
#
# class ScrollStatementGPT(BaseModel):
#     modified_statement: str
#
#
# class ScrollToType2GPT(BaseModel):
#     has_value_overlap: bool
#     overlapped_value: str
#     replaced_value: str
#     modified_test_code: str


class MutantInfoScrollType1GPT(BaseModel):
    original_node: str
    original_statement: str
    class_attribute_value: str
    qualified_nodes: list[str]
    modified_statements: list[str]


class MutantInfoScrollType2GPT(BaseModel):
    original_node: str
    original_expression: str
    class_attribute_value: str
    qualified_nodes: list[str]
    modified_expressions: list[str]


def collect_mutant_events_type3(event: TestEvent, assertions: list[TestAssertion],
                                xml_context_path: str) -> Tuple[list[MutantEvent], TestEvent] | None:
    """
    collect the mutant event for a scroll event
    :param event:
    :param assertions:
    :param xml_context_path:
    :return:
    """

    # step1. identify the scroll types
    scroll_type, scroll_info = identify_scroll_type(event.get_statement())

    # step2. build the full xml context path
    # the scroll event will get the next event's page source as context because this source contains the
    # scroll to target. The target may not be available before the scroll start
    full_xml_context_path: str = (f"{xml_context_path}/{event.get_test_method_name()}-event-{event.get_index() + 1}"
                                  f"-xml-content.xml")

    # check if the path is available
    if not os.path.exists(full_xml_context_path):
        print(f"The file at {full_xml_context_path} does not exist.")
        return None

    # step3. find mutant nodes and original node
    # collect the mutant nodes for type 1: scrollTo()
    origin_node = ""
    mutant_nodes = []
    mutant_statements = []

    if scroll_type is ScrollType.Type1:
        # step3.1. find all mutant nodes and the modified statements
        origin_node, mutant_nodes, mutant_statements = collect_mutant_info_scroll_type1(event.get_statement(),
                                                                                        full_xml_context_path)
        # step3.2. build xpath for origin event
        event.set_xpath(get_xpath_from_node(origin_node))

        # step3.3. for each mutant node, construct the MutantEvent object.
        mutant_events: list[MutantEvent] = construct_mutant_events(event, mutant_nodes, mutant_statements)

        # step3.4. collect before and after candidates for event
        event.set_mutant_candidates_before(count_number_of_nodes_in_xml_content(full_xml_context_path))
        event.set_mutant_candidates_after(len(mutant_events))

        return mutant_events, event

    # collect the mutant for type 2: scrollTo(matcher)
    elif scroll_type is ScrollType.Type2:
        # step3.1. find all mutant nodes and the modified statements
        origin_node, mutant_nodes, mutant_statements = collect_mutant_info_scroll_type2(event.get_statement(),
                                                                                        scroll_info,
                                                                                        full_xml_context_path)
        # step3.2. build xpath for origin event
        event.set_xpath(get_xpath_from_node(origin_node))

        # step3.3. for each mutant node, construct the MutantEvent object.
        mutant_events: list[MutantEvent] = construct_mutant_events(event, mutant_nodes, mutant_statements)

        # step3.4. collect before and after candidates for event
        event.set_mutant_candidates_before(count_number_of_nodes_in_xml_content(full_xml_context_path))
        event.set_mutant_candidates_after(len(mutant_events))

        return mutant_events, event
    else:
        raise ValueError(f"The scroll event type is undecided: {event.get_statement()}")


def collect_mutant_info_scroll_type1(statement, full_xml_context_path):
    user_prompt = \
        ("Which original node in the below xml tree does the statement: \"%s\" represents? "
         "What is the value of this original node's class attribute?"
         "Among all the rest node in this tree, what are the qualified nodes with same depth of this original node"
         " and have the same value of class attribute? "
         "If I want to replace the the original with each of the qualified node, how can I modify the statement? "
         "Please only update the argument value in this statement, do not add any new arguments. No explain.\n"
         "%s"
         % (statement, read_file_to_string(full_xml_context_path)))

    gpt_response = get_response_from_gpt(user_prompt, MutantInfoScrollType1GPT)

    response_json = json.loads(gpt_response.strip())

    return (response_json.get("original_node"), response_json.get("qualified_nodes"),
            response_json.get("modified_statements"))


def collect_mutant_info_scroll_type2(statement, scroll_info, full_xml_context_path):
    recycle_view_id = scroll_info.get("recycle_view_id")
    argument = scroll_info.get("argument")

    user_prompt = \
        ("Below is a xml tree of Android view hierarchy. "
         "A target node has resource-id value that contains \"%s\". "
         "Among all the target node's children nodes, there is one original node related to expression \"%s\". "
         "Among all the rest node in this tree, what are the qualified nodes with same depth of this original node"
         " and have the same value of class attribute? "
         "If I want to replace the original with each of the qualified node, how can I modify the expression? "
         "Please only update the argument value in this expression, do not add any new arguments. No explain.\n"
         "%s"
         % (recycle_view_id, argument, read_file_to_string(full_xml_context_path)))

    gpt_response = get_response_from_gpt(user_prompt, MutantInfoScrollType2GPT)

    response_json = json.loads(gpt_response.strip())

    modified_statements: list[str] = build_modified_statements_scroll_type2(statement,
                                                                            response_json.get("original_expression"),
                                                                            response_json.get("modified_expressions"))

    return (response_json.get("original_node"), response_json.get("qualified_nodes"),
            modified_statements)


def build_modified_statements_scroll_type2(statement, original_expression, modified_expressions) -> list[str]:
    """
    build the modified statements for mutant events based on modified expression in ScrollTo(matcher)
    :param statement: onView(withId(R.id.recycler_view)).perform(scrollTo(hasDescendant(withText("Clear all data"))));
    :param original_expression: hasDescendant(withText("Clear all data"))
    :param modified_expressions: hasDescendant(withText("Data"))
    :return: onView(withId(R.id.recycler_view)).perform(scrollTo(hasDescendant(withText("Data"))));
    """
    modified_statements: list[str] = []

    for modified_expression in modified_expressions:
        modified_statement = statement.replace(original_expression, modified_expression)
        modified_statements.append(modified_statement)
        print()

    return modified_statements


def construct_mutant_events(event, mutant_nodes, mutant_statements):
    mutant_events: list[MutantEvent] = []

    if mutant_nodes:  # have mutant
        count = 0
        for mutant_node in mutant_nodes:
            index: int = event.get_index()
            xpath: str = get_xpath_from_node(mutant_node)
            statement: str = mutant_statements[count]

            # skip the mutant event if it is the same with original event
            if is_identical_event(statement, event.get_statement()):
                continue

            mutant_event = MutantEvent(index, xpath, statement)
            mutant_events.append(mutant_event)
            count = count + 1

    return mutant_events


# def build_alter_event_statement_scroll_type1(sibling_node, origin_node, origin_statement):
#     """
#
#     :param sibling_node:
#     :param origin_node:
#     :param origin_statement:
#     :return:
#     """
#     matching_type = origin_node.get_matching_type()
#     alter_event_statement = ""
#
#     if sibling_node is not None:
#         if matching_type == ElementMatchingType.Type1:
#             alter_event_statement: str = get_alter_event_statement_match_type1(origin_node.get_node_value(),
#                                                                                sibling_node.get_node_value(),
#                                                                                origin_statement)
#         elif matching_type == ElementMatchingType.Type2 or matching_type == ElementMatchingType.Type3:
#             alter_event_statement: str = get_alter_event_statement_match_type2_3(origin_node.get_node_with_context(),
#                                                                                  sibling_node.get_node_with_context(),
#                                                                                  origin_statement)
#         else:
#             raise ValueError(f"ElementMatchingType is Type4, but sibling_node is not None: \n{origin_statement}")
#
#     else:
#         if matching_type == ElementMatchingType.Type4:
#             alter_event_statement: str = get_alter_event_statement_match_type4(origin_node.get_node_with_context(),
#                                                                                origin_statement)
#
#     if alter_event_statement:
#         return alter_event_statement
#     else:
#         return ""


# def get_alter_event_statement_match_type1(origin_node_value, sibling_node_value, origin_statement):
#     user_prompt = \
#         ("Below are two nodes from Android view hierarchy in xml. "
#          "The test statement \"%s\" "
#          "is performing a scrolling and related to the first node. "
#          "If I want to scroll to a similar view that related to the second node, how to modify the statement? "
#          "No explanation."
#          "%s\n"
#          "%s\n" % (origin_statement, origin_node_value, sibling_node_value))
#
#     gpt_response = get_response_from_gpt(user_prompt, ScrollStatementGPT)
#
#     response_json = json.loads(gpt_response.strip())
#
#     return response_json.get("modified_statement")


# def get_alter_event_statement_match_type2_3(origin_node_context, sibling_node_context, origin_statement):
#     user_prompt = \
#         ("Below are two xml subtrees that represent Android view hierarchy. "
#          "The first one is related to Android espresso statement that performing a scrolling: "
#          "\"%s\", "
#          "If I want to modify this statement to perform a similar scrolling using the second xml tree, "
#          "How I can modify the matcher in the statement? \n"
#          "Do not add any new view matchers, only update the current matchers' values."
#          "%s\n%s" % (origin_statement, origin_node_context, sibling_node_context))
#
#     gpt_response = get_response_from_gpt(user_prompt, ScrollStatementGPT)
#
#     response_json = json.loads(gpt_response.strip())
#
#     return response_json.get("modified_statement")


# def get_alter_event_statement_match_type4(origin_node_context, origin_statement):
#     user_prompt = \
#         ("Below is an xml tree that represent Android view hierarchy. "
#          "The Android espresso statement "
#          "\"%s\" is related to one of the node in this xml tree. "
#          "If I want to rewrite this statement using a different node in the tree, "
#          "How I can modify the matcher in the statement? \n"
#          "Do not add any new view matchers, only update the current matchers' values. "
#          "If cannot rewrite, leave the output statement empty.\n"
#          "%s" % (origin_statement, origin_node_context))
#
#     gpt_response = get_response_from_gpt(user_prompt, ScrollStatementGPT)
#
#     response_json = json.loads(gpt_response.strip())
#
#     return response_json.get("modified_statement")


# def get_alter_event_statement_scroll_type1_request(origin_statement, sibling_node, origin_node):
#     user_prompt = \
#         ("Below are two nodes from Android view hierarchy in xml. "
#          "The test statement \"%s\" "
#          "is related to the first node. "
#          "If I want to design a similar statement on the second node, how to update the statement? "
#          "No explanation."
#          "%s\n"
#          "%s\n" % (origin_statement, origin_node, sibling_node))
#
#     return get_response_from_gpt(user_prompt, ScrollStatementGPT)


# def construct_mutant_scroll_events_type2(argument, event, origin_node, sibling_nodes, full_xml_context_path):
#     xml_context = read_file_to_string(full_xml_context_path)
#
#     mutant_events: list[MutantEvent] = []
#     origin_node_with_descendant: str = collect_descendant_of_node(origin_node, xml_context)
#     for sibling_node in sibling_nodes:
#         index: int = event.get_index()
#         xpath: str = build_xpath_from_xml_node(sibling_node, full_xml_context_path)
#         sibling_node_with_descendant: str = collect_descendant_of_node(sibling_node, xml_context)
#         statement: str = build_alter_event_statement_scroll_type2(sibling_node_with_descendant,
#                                                                   origin_node_with_descendant,
#                                                                   argument)
#         assertion_statement: str = ""
#
#         mutant_event = MutantEvent(index, xpath, statement, assertion_statement)
#         mutant_events.append(mutant_event)
#
#     return mutant_events


# def build_alter_event_statement_scroll_type2(sibling_node, origin_node, argument):
#     gpt_response = get_alter_event_statement_scroll_type2_request(argument, sibling_node, origin_node)
#     alter_event_statement: str = get_alter_event_statement_scroll_type2_request_handler(gpt_response)
#
#     if alter_event_statement:
#         return alter_event_statement
#     else:
#         return ""


# def get_alter_event_statement_scroll_type2_request(argument, sibling_node, origin_node):
#     user_prompt = \
#         ("Below are two nodes and their descendant from Android view hierarchy in xml. "
#          "The test code \"%s\" "
#          "is related to the first node and its descendant. "
#          "What value is overlapped between this test code and the first node and its descendant?"
#          "If I want to rewrite the test code using the second node and its descendant, "
#          "what value should I replace? What is the modified test code?\n"
#          "No explanation."
#          "%s\n"
#          "%s\n" % (argument, origin_node, sibling_node))
#
#     return get_response_from_gpt(user_prompt, ScrollStatementGPT)
#
#
# def get_alter_event_statement_scroll_type2_request_handler(gpt_response):
#     # step 1. convert the response string to json object
#     response_json = json.loads(gpt_response.strip())
#
#     # step 2. get results
#     return response_json.get("sibling_statement")


def identify_scroll_type(statement: str) -> Tuple[ScrollType, json]:
    scroll_info: json = identify_scroll_type_request(statement)

    if scroll_info.get("is_recycle_view"):
        if scroll_info.get("scroll_to_has_argument"):
            return ScrollType.Type2, scroll_info
        else:
            raise ValueError(f"Scroll Type not supported: {statement}")
    else:
        if not scroll_info.get("scroll_to_has_argument"):
            return ScrollType.Type1, scroll_info
        else:
            raise ValueError(f"Scroll Type not supported: {statement}")


def identify_scroll_type_request(statement: str):
    user_prompt = \
        ("Below is java code. "
         "Does the first statement include matching a recycle view id? If so, what is the id value? "
         "Does the statement invoke scrollTo method? "
         "If yes, does this method has argument? What is the argument? "
         "%s" % statement)

    gpt_response = get_response_from_gpt(user_prompt, ScrollTypeGPT)

    # step 1. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 2. return results
    if response_json:
        return response_json
    else:
        raise ValueError(f"Scroll Info is empty: {response_json}")


# def collect_event_sibling_nodes_scroll_type1(event_statement, full_xml_context_path) -> tuple[str, list[str]]:
#     gpt_response: str = collect_event_sibling_nodes_scroll_type1_request(event_statement, full_xml_context_path)
#     return collect_event_sibling_nodes_scroll_type1_request_handler(gpt_response)


# def collect_event_sibling_nodes_scroll_type1_request(statement, full_xml_context_path):
#     # read the xml tree content
#     xml_context = read_file_to_string(full_xml_context_path)
#
#     # prepare user prompt
#     user_prompt = \
#         ("The statement \"%s\" is scrolling to an UI element that meets given matcher. "
#          "Which node in the below xml tree does this statement represent? "
#          "What is the value of this node's class attribute? "
#          "What are all the rest nodes with same depth of this node and have the same value of class attribute? "
#          "%s" % (statement, xml_context))
#
#     return get_response_from_gpt(user_prompt, ScrollNodeType1GPT)


# def collect_event_sibling_nodes_scroll_type1_request_handler(gpt_response) -> Tuple[str, list[str]]:
#     # step 1. convert the response string to json object
#     response_json = json.loads(gpt_response.strip())
#
#     # step 2. get results
#     original_node = response_json.get("node")
#     sibling_nodes = response_json.get("same_depth_nodes_with_same_class")
#
#     return original_node, sibling_nodes


# def collect_event_sibling_nodes_scroll_type2(scroll_info, full_xml_context_path):
#     gpt_response: str = collect_event_sibling_nodes_scroll_type2_request(scroll_info, full_xml_context_path)
#     return collect_event_sibling_nodes_scroll_type2_request_handler(gpt_response)


# def collect_event_sibling_nodes_scroll_type2_request(scroll_info, full_xml_context_path):
#     """
#     collect the sibling nodes for scrollTo(matcher) in recycle view
#     :param scroll_info:
#     :param full_xml_context_path:
#     :return:
#     """
#     # read the xml tree content
#     xml_context = read_file_to_string(full_xml_context_path)
#
#     # prepare user prompt
#     user_prompt = \
#         ("A statement is scrolling to an UI element that meets the matcher \"%s\", "
#          "and also has an ancestor with id contains \"%s\""
#          "Which nodes in the below xml tree might represent this statement? "
#          "Output the node. "
#          "What is the value of this node's class attribute? "
#          "What are all the rest nodes with same depth of this node, share same ancestor, "
#          "and have the same value of class attribute? \n"
#          "%s" % (scroll_info.get("argument"), scroll_info.get("recycle_view_id"), xml_context))
#
#     return get_response_from_gpt(user_prompt, ScrollNodeType1GPT)


# def collect_event_sibling_nodes_scroll_type2_request_handler(gpt_response) -> Tuple[str, list[str]]:
#     # step 1. convert the response string to json object
#     response_json = json.loads(gpt_response.strip())
#
#     # step 2. get results
#     original_node = response_json.get("node")
#     sibling_nodes: list[str] = response_json.get("same_depth_nodes_with_same_class")
#
#     return original_node, sibling_nodes


# collect the siblings for type 1: scrollTo()
# def construct_mutant_scroll_events_type1(event, origin_node, sibling_nodes, full_xml_context_path):
#     mutant_events: list[MutantEvent] = []
#
#     if sibling_nodes:  # event has siblings
#         for sibling_node in sibling_nodes:
#             index: int = event.get_index()
#             xpath: str = build_xpath_from_xml_node(sibling_node, full_xml_context_path)
#             statement: str = build_alter_event_statement_scroll_type1(sibling_node, origin_node, event.get_statement())
#
#             mutant_event = MutantEvent(index, xpath, statement)
#             mutant_events.append(mutant_event)
#     else:
#         index: int = event.get_index()
#         statement: str = build_alter_event_statement_scroll_type1(None, origin_node, event.get_statement())
#         xpath: str = build_xpath_from_statement(statement, full_xml_context_path)
#
#         mutant_event = MutantEvent(index, xpath, statement)
#         mutant_events.append(mutant_event)
#
#     return mutant_events
