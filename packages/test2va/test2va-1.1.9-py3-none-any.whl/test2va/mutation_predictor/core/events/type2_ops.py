import json
import os
from typing import Tuple

from pydantic import BaseModel

from test2va.mutation_predictor.core.basic_test.MutantEvent import MutantEvent
from test2va.mutation_predictor.core.basic_test.TestAssertion import TestAssertion
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent
from test2va.mutation_predictor.core.events.common_ops import (build_xpath_from_statement,
                                                               count_number_of_nodes_in_xml_content,
                                                               is_identical_event)
from test2va.mutation_predictor.core.mutant_operator.control_mutator import ControlMutator


class AlterTypedInValuesGPT(BaseModel):
    can_replaced: bool
    alternative_values: list[str]


class Type2StatementGPT(BaseModel):
    updated_statement: str


def collect_mutant_events_type2(event: TestEvent, events: list[TestEvent], assertions: list[TestAssertion],
                                xml_context_path: str) -> Tuple[list[MutantEvent], TestEvent] | None:
    """
    Collect the mutant event candidates of a typed-in event.
    Mutant type-in event will have same xpath but different typed value.

    :param events:
    :param event:
    :param assertions:
    :param xml_context_path:
    :return:
    """

    # step1. build the full xml context path
    full_xml_context_path: str = (f"{xml_context_path}/{event.get_test_method_name()}-event-{event.get_index()}"
                                  f"-xml-content.xml")

    # check if the path is available
    if not os.path.exists(full_xml_context_path):
        print(f"The file at {full_xml_context_path} does not exist.")
        return None

    # step2. build xpath for origin event
    event.set_xpath(build_xpath_from_statement(event.get_statement(), full_xml_context_path))

    # # step3.old. collect three alternative typed-in values.
    # overlap_value: str = event.get_overlap_value()
    # alter_values: list[str] = collect_alter_typed_in_values_type2(overlap_value, event, events, assertions)

    # step3. apply the control mutator to generate mutant actions.
    mutant_statements = ControlMutator.collect_control_mutants_type_in_action(event, events)

    # step4. for each alternative value, construct the MutantEvent object.
    mutant_events: list[MutantEvent] = construct_mutant_events(event, mutant_statements)

    # step5. collect before and after candidates for event (optional)
    event.set_mutant_candidates_before(count_number_of_nodes_in_xml_content(full_xml_context_path))
    event.set_mutant_candidates_after(len(mutant_events))

    return mutant_events, event

def construct_mutant_events(event, mutant_statements):

    mutant_events: list[MutantEvent] = []
    for mutant_statement in mutant_statements:
        index: int = event.get_index()
        xpath: str = event.get_xpath()  # mutant type-in event will have same xpath but different typed value.

        # skip the mutant event if it is the same with original event
        if is_identical_event(mutant_statement, event.get_statement()):
            continue

        mutant_event = MutantEvent(index, xpath, mutant_statement)
        mutant_events.append(mutant_event)

    return mutant_events

#
# def build_alter_event_statement_type2(value, overlap_value, origin_statement):
#     gpt_response = get_alter_event_statement_request(value, overlap_value, origin_statement)
#     alter_event_statement: str = get_alter_event_statement_request_handler(gpt_response)
#
#     if alter_event_statement:
#         return alter_event_statement
#     else:
#         return ""
#
#
# def get_alter_event_statement_request(value, overlap_value, origin_statement):
#     user_prompt = \
#         ("The test statement \"%s\" is typing in value of \"%s\". "
#          "If I want to replace this value to \"%s\", how to update this statement? "
#          "No explanation." % (origin_statement, overlap_value, value))
#
#     return get_response_from_gpt(user_prompt, Type2StatementGPT)
#
#
# def get_alter_event_statement_request_handler(gpt_response):
#     # step 1. convert the response string to json object
#     response_json = json.loads(gpt_response.strip())
#
#     # step 2. get results
#     return response_json.get("updated_statement")
#
#
# def collect_alter_typed_in_values_type2(overlap_value: str, event: TestEvent,
#                                         events: list[TestEvent], assertions: list[TestAssertion]) -> list[str]:
#     # step1. form the test code: list of event + related assertion
#     test_code: str = build_event_code_segment(events)
#
#     # step2. collect alternative typed-in value
#     response: str = collect_alter_typed_in_values_request(test_code, overlap_value)
#     alter_values: list[str] = collect_alter_typed_in_values_request_handler(response)
#
#     return alter_values
#
#
# def collect_alter_typed_in_values_request(test_code, overlap_value):
#     user_prompt = \
#         ("In the below test code, one of the statement is typing in value of \"%s\". "
#          "Can this value be replaced? "
#          "If yes, can you give me three alternative replacement values by "
#          "following the same format of original value?\n"
#          "%s" % (overlap_value, test_code))
#
#     return get_response_from_gpt(user_prompt, AlterTypedInValuesGPT)
#
#
# def collect_alter_typed_in_values_request_handler(response) -> list[str]:
#     # step 1. convert the response string to json object
#     response_json = json.loads(response.strip())
#
#     # step 2. get results
#     if response_json.get("can_replaced"):
#         return response_json.get("alternative_values")
