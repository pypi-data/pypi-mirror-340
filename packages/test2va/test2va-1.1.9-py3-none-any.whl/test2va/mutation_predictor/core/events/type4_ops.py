import os
from typing import Tuple

from pydantic import BaseModel

from test2va.mutation_predictor.core.basic_test.MutantEvent import MutantEvent
from test2va.mutation_predictor.core.basic_test.TestAssertion import TestAssertion
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent
from test2va.mutation_predictor.core.events.common_ops import build_xpath_from_statement, \
    is_identical_event, get_xpath_from_node
from test2va.mutation_predictor.core.mutant_operator.control_mutator import ControlMutator
from test2va.mutation_predictor.core.mutant_operator.element_mutator import ElementMutator



class Type4StatementGPT(BaseModel):
    updated_statement: str


def collect_mutant_events_type4(event: TestEvent, assertions: list[TestAssertion],
                                xml_context_path: str) -> Tuple[list[MutantEvent], TestEvent] | None:
    """
    Collect the mutant for swipe event.
    Mutant swipe event has two types:
        1. same swipe action but on a different element(xpath)
        2. same xpath but different swipe action.
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

    # step3-1. apply the element mutator to find all mutant nodes with the same action
    origin_node, mutant_nodes, mutant_statements_type1 = ElementMutator.collect_element_mutants(event.get_statement(),
                                                                                          full_xml_context_path)

    # step3-2. for each mutant node, construct the MutantEvent object.
    mutant_events: list[MutantEvent] = construct_mutant_events_type1(event, mutant_nodes, mutant_statements_type1)

    # step4-1. apply the control mutator to find same nodes with the different action
    mutant_statement_type2 = ControlMutator.collect_control_mutants_swipe_action(event)

    # step4-2. construct the mutant object and append
    mutant_events.append(construct_mutant_events_type2(event, mutant_statement_type2))

    return mutant_events, event


def construct_mutant_events_type2(event, mutant_statement):
    index: int = event.get_index()
    xpath: str = event.get_xpath()

    if not is_identical_event(mutant_statement, event.get_statement()):
        mutant_event = MutantEvent(index, xpath, mutant_statement)
        return mutant_event
    else:
        return None


def construct_mutant_events_type1(event, mutant_nodes, mutant_statements):

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

# def build_alter_event_statement_type4(origin_statement):
#     gpt_response = get_alter_event_statement_request(origin_statement)
#     alter_event_statement: str = get_alter_event_statement_request_handler(gpt_response)
#
#     if alter_event_statement:
#         return alter_event_statement
#     else:
#         return ""
#
#
# def get_alter_event_statement_request(origin_statement: str):
#     user_prompt = \
#         ("The test statement \"%s\" "
#          "is performing a swipe action."
#          "Please update the statement so that the swipe action will be performed "
#          "on the same UI element but opposite direction. "
#          "No explanation." % origin_statement)
#
#     return get_response_from_gpt(user_prompt, Type4StatementGPT)
#
#
# def get_alter_event_statement_request_handler(gpt_response):
#     # step 1. convert the response string to json object
#     response_json = json.loads(gpt_response.strip())
#
#     # step 2. get results
#     return response_json.get("updated_statement")
