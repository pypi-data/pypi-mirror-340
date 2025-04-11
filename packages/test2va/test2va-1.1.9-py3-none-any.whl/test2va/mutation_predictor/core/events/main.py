from typing import Tuple

from openai import OpenAI

from test2va.mutation_predictor.core.assertions.common_ops import build_mutant_assertion_statement, \
    update_value_overlap_by_assertion, build_mutant_assertion_statements, build_assertions_list_str
from test2va.mutation_predictor.core.basic_test.MutantEvent import MutantEvent
from test2va.mutation_predictor.core.basic_test.TestAssertion import TestAssertion
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent
from test2va.mutation_predictor.core.basic_test.TestMethod import TestMethod
from test2va.mutation_predictor.core.basic_test.TestTypes import EventType
from test2va.mutation_predictor.core.events.common_ops import identify_event_type, get_related_assertion, \
    is_identical_event
from test2va.mutation_predictor.core.events.type1_ops import collect_mutant_events_type1
from test2va.mutation_predictor.core.events.type2_ops import collect_mutant_events_type2
from test2va.mutation_predictor.core.events.type3_ops import collect_mutant_events_type3
from test2va.mutation_predictor.core.events.type4_ops import collect_mutant_events_type4


def generate_mutant_event_candidates(origin_assertions: list[TestAssertion], events: list[TestEvent],
                                     xml_context_path: str, method: TestMethod) -> list[TestEvent]:
    """
    This overall method to generate event candidates with or without the assertion updates.
    :param method: original test method
    :param origin_assertions: a list of TestAssertion
    :param events: a list of TestEvents
    :param xml_context_path: page resource (xml hierarchy) of the event
    :return: updated a list of TestEvents with mutant information
    """

    # step 1. figure out value overlapped in all events and assertions, only overlapped assertion need to be updated.
    assertions, events = update_value_overlap_by_assertion(origin_assertions, events)

    # step 2. iterate all events to collect the mutant candidates
    for event in events:

        # 2.1 identify type
        event_type: EventType = identify_event_type(event)

        # 2.2 collect mutants events and the assertion if overlap exist.
        result = collect_mutant_events(event, events, assertions, xml_context_path, event_type)

        # Check if the mutant result is None
        if result is None:
            continue
        else:
            # 2.2.1 collect mutant events
            mutant_events, event = result
            event.set_mutant_events(mutant_events)

            # 2.2.2 collect the updated mutant assertion if value overlapped
            if event.get_has_overlap():
                for mutant_event in mutant_events:
                    mutant_assertions: list[str] = build_mutant_assertion_statements(mutant_event, event, method, assertions)
                    mutant_event.set_assertion_statement_pairs(mutant_assertions, build_assertions_list_str(assertions))

            # # if the event's value overlap with the assertion, collect the updated assertion for mutant event.
            # if event.get_has_overlap():
            #     # get the related assertion
            #     relate_assertion = get_related_assertion(event, assertions)
            #
            #     # if relate_assertion is not None:
            #     if relate_assertion:
            #         for mutant_event in mutant_events:
            #             mutant_assertion_statement = build_mutant_assertion_statement(mutant_event, event,
            #                                                                           relate_assertion, events)
            #             mutant_event.set_assertion_statement(mutant_assertion_statement)

    return events


def collect_mutant_events(event: TestEvent, events: list[TestEvent], assertions: list[TestAssertion],
                          xml_context_path: str, event_type: EventType) -> Tuple[list[MutantEvent], TestEvent] | None:
    """
    Collect the mutant events based on the context and the predicted type.
    :param events: a list of events from test method.
    :param event: the target event which we are collecting the mutant.
    :param assertions: a list of assertions from test method.
    :param xml_context_path: page source path.
    :param event_type:  EventType of the original TestEvent event
    :return: the collected mutant event and updated original event
    """
    # apply different mutant event collector on different type
    if event_type is EventType.Type1:  # click event
        return collect_mutant_events_type1(event, assertions, xml_context_path)
    elif event_type is EventType.Type2:  # typed-in event
        return collect_mutant_events_type2(event, events, assertions, xml_context_path)
    elif event_type is EventType.Type3:  # scroll event
        return collect_mutant_events_type3(event, assertions, xml_context_path)
    elif event_type is EventType.Type4:  # swipe event
        return collect_mutant_events_type4(event, assertions, xml_context_path)
    else:
        raise ValueError(f"The event type in statement is not supported {event.get_statement()}")

