import os
from typing import Tuple

from test2va.mutation_predictor.core.basic_test.MutantEvent import MutantEvent
from test2va.mutation_predictor.core.basic_test.TestAssertion import TestAssertion
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent
from test2va.mutation_predictor.core.events.common_ops import get_xpath_from_node, count_number_of_nodes_in_xml_content, is_identical_event
from test2va.mutation_predictor.core.mutant_operator.element_mutator import ElementMutator



# class Type1StatementGPT(BaseModel):
#     modified_statement: str


# class MutantInfoType1GPT(BaseModel):
#     original_node: str
#     original_statement: str
#     class_attribute_value: str
#     qualified_nodes: list[str]
#     modified_statements: list[str]


def collect_mutant_events_type1(event: TestEvent, assertions: list[TestAssertion],
                                xml_context_path: str) -> Tuple[list[MutantEvent], TestEvent] | None:
    """
    Collect the mutant event candidate of a click event

    :param event:
    :param assertions:
    :param xml_context_path:
    :return: a list of mutant events and the updated original event
    """

    # step1. build the full xml context path
    full_xml_context_path: str = (f"{xml_context_path}/{event.get_test_method_name()}-event-{event.get_index()}"
                                  f"-xml-content.xml")

    # check if the path is available
    if not os.path.exists(full_xml_context_path):
        print(f"The file at {full_xml_context_path} does not exist.")
        return None

    # step2. apply the element mutator to find all mutant nodes.
    origin_node, mutant_nodes, mutant_statements = ElementMutator.collect_element_mutants(event.get_statement(),
                                                                             full_xml_context_path)

    # step3. build xpath for origin event
    event.set_xpath(get_xpath_from_node(origin_node))

    # step4. for each mutant node, construct the MutantEvent object.
    mutant_events: list[MutantEvent] = construct_mutant_events(event, mutant_nodes, mutant_statements)

    # step5. collect before and after candidates for event (optional)
    event.set_mutant_candidates_before(count_number_of_nodes_in_xml_content(full_xml_context_path))
    event.set_mutant_candidates_after(len(mutant_events))

    return mutant_events, event


# def collect_mutant_info_type1(statement, full_xml_context_path):
#
#     user_prompt = \
#         ("Which original node in the below xml tree does the statement: \"%s\" represents? "
#          "What is the value of this original node's class attribute?"
#          "Among all the rest node in this tree, what are all the qualified nodes with same depth of this original node"
#          " and have the same value of class attribute? "
#          "If I want to replace the original with each of the qualified nodes, how can I modify the statement? "
#          "Please only update the argument value in this statement, do not add any new arguments. No explain.\n"
#          "%s"
#          % (statement, read_file_to_string(full_xml_context_path)))
#
#     gpt_response = get_response_from_gpt(user_prompt, MutantInfoType1GPT)
#
#     response_json = json.loads(gpt_response.strip())
#
#     return (response_json.get("original_node"), response_json.get("qualified_nodes"),
#             response_json.get("modified_statements"))


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


