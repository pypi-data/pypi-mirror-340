import json
from typing import Tuple

from pydantic import BaseModel

from test2va.mutation_predictor.core.basic_test.MutantEvent import MutantEvent
from test2va.mutation_predictor.core.basic_test.TestAssertion import TestAssertion
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent
from test2va.mutation_predictor.core.basic_test.TestMethod import TestMethod
from test2va.mutation_predictor.core.events.common_ops import build_events_str_list
from test2va.mutation_predictor.util.gpt_util import get_response_from_gpt
from test2va.mutation_predictor.util.util import list_to_str


class UpdateAssertionGPT(BaseModel):
    assertion_statement: str


class MutantAssertionsGPT(BaseModel):
    modified_assertion_statements: list[str]


class ValueOverlapGPT(BaseModel):
    is_overlap: bool
    overlapped_values: list[str]
    overlapped_statements: list[str]


def build_mutant_assertion_statements(mutant_event: MutantEvent, event: TestEvent,
                                      method: TestMethod, assertions: list[TestAssertion]) -> list[str]:
    # user_prompt = \
    #     ("%s\n"
    #      "In the above Android GUI java test code using Espresso, "
    #      "If I want to replace the statement \"%s\" to \"%s\", "
    #      "how to update the below assertion statements so that they still pass? "
    #      "Do not add new arguments. "
    #      "No explain. Please output the modified statements as a list.\n"
    #      % (method.get_method_str(), event.get_statement(), mutant_event.get_statement()))

    user_prompt = '''%s
    In the above Android GUI java test code using Espresso, 
    If I want to replace the statement "%s" to "%s", 
    how to update the below assertion statements so that they still pass? 
    Do not add new arguments. No explain. Please output the modified assertions as a list.
    The modified assertions should have the same length of the original assertions.

    %s
    ''' % (method.get_method_str(), event.get_statement(),
           mutant_event.get_statement(), list_to_str(build_assertions_list_str(assertions)))

    print(user_prompt)

    gpt_response = get_response_from_gpt(user_prompt, MutantAssertionsGPT)

    # process the response
    response_json = json.loads(gpt_response.strip())

    return response_json.get("modified_assertion_statements")


def build_assertions_list_str(assertions: list[TestAssertion]):
    """
    Build a string representation of assertion list.
    :param assertions:
    :return:
    """
    str_list: list[str] = []
    for assertion in assertions:
        str_list.append(assertion.get_statement())

    return str_list


def build_mutant_assertion_statement(mutant_event: MutantEvent, event: TestEvent,
                                     assertion: TestAssertion, origin_events: list[TestEvent]) -> str:

    # step1. build test code segment
    test_code = build_test_code_segment(origin_events, assertion)

    # step2. collect mutant statement
    response = collect_mutant_assertion_request(test_code, event.get_statement(), mutant_event.get_statement())
    return collect_mutant_assertion_request_handler(response)


def collect_mutant_assertion_request(test_code: str, event_statement: str, mutant_statement: str):
    user_prompt = \
        ("In the below Android GUI java test code using Espresso, "
         "the last assertion statement is examining: "
         "\"%s\" from the earlier statements."
         "If I replace this statement to \"%s\", "
         "How to update the last assertion statement so that the assertion still pass? "
         "No explain.\n"
         "%s\n" % (event_statement, mutant_statement, test_code))

    return get_response_from_gpt(user_prompt, UpdateAssertionGPT)


def collect_mutant_assertion_request_handler(response):
    # step 1. convert the response string to json object
    response_json = json.loads(response.strip())

    # step 2. get results
    return response_json.get("assertion_statement")


def build_test_code_segment(events: list[TestEvent], related_assertion: TestAssertion) -> str:
    """
    Given original list of event and list of assertion, build the test code segment for the target event.

    :param events:
    :param related_assertion:
    :return: test code segment as string
    """

    # prepare the event code
    events_str: list[str] = build_events_str_list(events)
    event_test_code: str = list_to_str(events_str)

    # prepare the assertion code
    if related_assertion:
        assertion_test_code: str = related_assertion.get_statement()
    else:
        assertion_test_code: str = ""

    test_code = f"{event_test_code}\n{assertion_test_code}"

    return test_code


def update_value_overlap_by_assertion(assertions: list[TestAssertion], events: list[TestEvent]) \
        -> Tuple[list[TestAssertion], list[TestEvent]]:
    """
    Compare the value in test events, and see if some of the value is overlapped with assertion statements.
    The overlap will be used to indicate a potential asserted.

    :param assertions:
    :param events:
    :return:
    """
    index = 0
    for assertion in assertions:
        is_overlap, overlap_events_str, overlap_values = find_value_overlaps(assertion, events)

        # update is_value_overlapped
        assertion.set_is_value_overlapped(is_overlap)

        # update related event in assertion
        assertion.add_related_events_indices_by_overlap(events, overlap_events_str)

        # update the related assertion in event
        for event in events:
            event.add_related_assertion_indices_by_overlap(index, overlap_events_str)
            event.set_overlap_value_by_overlap_report(overlap_values)

        index = index + 1

    return assertions, events


def update_event_assertion_by_value_overlap(assertions: list[TestAssertion], events: list[TestEvent]) \
        -> Tuple[list[TestAssertion], list[TestEvent]]:
    """
    Compare the value in test events, and see if some of the value is overlapped with assertion statements.
    The overlap will be used to indicate a potential asserted.

    :param assertions:
    :param events:
    :return:
    """
    index = 0
    for assertion in assertions:
        is_overlap, overlap_events_str, overlap_values = find_value_overlaps(assertion, events)

        # update is_value_overlapped
        assertion.set_is_value_overlapped(is_overlap)

        # update related event in assertion
        assertion.add_related_events_indices_by_overlap(events, overlap_events_str)

        # update the related assertion in event
        for event in events:
            event.add_related_assertion_indices_by_overlap(index, overlap_events_str)
            event.set_overlap_value_by_overlap_report(overlap_values)

        index = index + 1

    return assertions, events


def find_value_overlaps(assertion, events) -> Tuple[bool, list[str], list[str]]:

    user_prompt \
        = ("In the below java test code, does the value the last statement is checking overlaps or "
           "partially overlaps with the values in any of the earlier statements? "
           "If so, what is the value that it is checking, and what are the overlapped statements? "
           "Please keep the semicolon, no explanation. \n"
           "%s\n%s\n" % (list_to_str(build_events_str_list(events)),
                         assertion.get_statement()))

    gpt_response = get_response_from_gpt(user_prompt, ValueOverlapGPT)

    # step 1. convert the response string to json object
    response_json = json.loads(gpt_response.strip())

    # step 2. get is_overlap
    is_overlap: bool = response_json.get("is_overlap")
    overlap_events_str: list[str] = response_json.get("overlapped_statements")
    overlap_values = response_json.get("overlapped_values")

    return is_overlap, overlap_events_str, overlap_values
