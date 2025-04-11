import json
from pydantic import BaseModel

from test2va.mutation_predictor.core.basic_test import TestEvent
from test2va.mutation_predictor.core.events.common_ops import build_event_code_segment
from test2va.mutation_predictor.util.gpt_util import get_response_from_gpt


class AlterTypedInValuesGPT(BaseModel):
    can_replaced: bool
    alternative_values: list[str]


class UpdatedStatementGPT(BaseModel):
    updated_statement: str



class ControlMutator:

    @staticmethod
    def collect_control_mutants_type_in_action(event: TestEvent, events: list[TestEvent]):
        """
        apply the control mutant operators for typed-in action: input different contents
        :param event: original target input event
        :param events: all other events in the original method
        :return:
        """
        alter_values: list[str] = ControlMutator._collect_alter_typed_in_values(event, events)
        mutant_statements: list[str] = []
        for alter_value in alter_values:
            mutant_statement = ControlMutator._build_alter_typed_in_statement(alter_value,
                                                                             event.get_overlap_value(),
                                                                             event.get_original_statement())
            mutant_statements.append(mutant_statement)

        return mutant_statements

    @staticmethod
    def collect_control_mutants_swipe_action(event: TestEvent):
        """
        apply the control mutant operators for swipe action: different direction
        :param event: the original event
        :return:
        """
        return ControlMutator._build_alter_swipe_statement_gpt(event.get_statement())


    ######################## Below are all helper and internal methods #########################

    @staticmethod
    def _build_alter_swipe_statement_gpt(origin_statement):

        user_prompt = \
            ("The test statement \"%s\" "
             "is performing a swipe action."
             "Please update the statement so that the swipe action will be performed "
             "on the same UI element but opposite direction. "
             "No explanation." % origin_statement)

        response = get_response_from_gpt(user_prompt, UpdatedStatementGPT)

        # step 1. convert the response string to json object
        response_json = json.loads(response.strip())

        # step 2. get results
        if response_json.get("updated_statement"):
            return response_json.get("updated_statement")
        else:
            return ""


    @staticmethod
    def _collect_alter_typed_in_values(event: TestEvent, events: list[TestEvent]) -> list[str]:
        # step1. form the test code: list of event + related assertion
        test_code: str = build_event_code_segment(events)

        # step2. collect entered content of the target typed in action
        overlap_value: str = event.get_overlap_value()

        # step2. collect alternative entered contents
        alter_values: list[str] = ControlMutator._collect_alter_typed_in_values_gpt(test_code, overlap_value)

        return alter_values

    @staticmethod
    def _collect_alter_typed_in_values_gpt(test_code, overlap_value):
        user_prompt = \
            ("In the below test code, one of the statement is typing in value of \"%s\". "
             "Can this value be replaced? "
             "If yes, can you give me three alternative replacement values by "
             "following the same format of original value?\n"
             "%s" % (overlap_value, test_code))

        response = get_response_from_gpt(user_prompt, AlterTypedInValuesGPT)

        response_json = json.loads(response.strip())

        # step 2. get results
        if response_json.get("can_replaced"):
            return response_json.get("alternative_values")


    @staticmethod
    def _build_alter_typed_in_statement(alter_value, original_value, origin_statement):

        user_prompt = \
            ("The test statement \"%s\" is typing in value of \"%s\". "
             "If I want to replace this value to \"%s\", how to update this statement? "
             "No explanation." % (origin_statement, original_value, alter_value))

        gpt_response = get_response_from_gpt(user_prompt, UpdatedStatementGPT)

        # step 1. convert the response string to json object
        response_json = json.loads(gpt_response.strip())

        # step 2. get results
        if response_json.get("updated_statement"):
            return response_json.get("updated_statement")
        else:
            return ""


