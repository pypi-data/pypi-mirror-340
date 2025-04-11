"""
    This module is going to extract the basic test method in raw test file,
    And then separate the test action list and assertion list
"""
import json

from pydantic import BaseModel

from test2va.mutation_predictor.core.basic_test.TestAssertion import TestAssertion
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent
from test2va.mutation_predictor.core.basic_test.TestMethod import TestMethod
from test2va.mutation_predictor.util.gpt_util import get_response_from_gpt


class BaseTestStatementGPT(BaseModel):
    test_method_name: str
    test_event_statement_list: list[str]
    test_assertion_statement_list: list[str]


class BaseTestMethodGPT(BaseModel):
    has_before_method: bool
    before_method: str
    test_method: str
    test_method_name: str


def base_test_statements_build_request(raw_file: str) \
        -> tuple[list[TestAssertion], list[TestEvent]]:

    user_prompt = \
        ("Below is an Android GUI java test method with Espresso framework. "
         "Among all the statement start with \"onView\", "
         "which statements are test events and which of them are test assertions? "
         "Please extract the statements and method name. Please keep the semicolon for each statement.\n"
         "%s" % raw_file)

    gpt_response_content = get_response_from_gpt(user_prompt, BaseTestStatementGPT)

    test_events: list[TestEvent] = []
    test_assertions: list[TestAssertion] = []

    # convert gpt response to json
    response_json = json.loads(gpt_response_content.strip())

    # get method name
    method_name: str = response_json.get("test_method_name")

    # get event list and build test event
    test_event_list_response: list[str] = response_json.get("test_event_statement_list")
    if test_event_list_response is None:
        # Handle the case where `test_event_list_response` is None
        print("Error: test_event_list_response is None.")
    else:
        # create event list
        index = 0
        for response in test_event_list_response:
            test_event: TestEvent = TestEvent()
            test_event.set_test_method_name(method_name)  # update method
            test_event.set_index(index)  # update index
            test_event.set_statement(response)  # update statement str

            test_events.append(test_event)
            index = index + 1

    # get assertion list
    test_assertion_list_response: list[str] = response_json.get("test_assertion_statement_list")
    if test_assertion_list_response is None:
        # Handle the case where `test_event_list_response` is None
        print("Error: test_assertion_statement_list is None.")
    else:
        # create assertion list
        index = 0
        for response in test_assertion_list_response:
            test_assertion: TestAssertion = TestAssertion()
            test_assertion.set_test_method_name(method_name)  # update method
            test_assertion.set_index(index)  # update index
            test_assertion.set_statement(response)  # update statement str

            test_assertions.append(test_assertion)
            index = index + 1

    return test_assertions, test_events


def base_test_method_build_request(raw_file: str) -> str:
    user_prompt = \
        ("In the below java class for Android espresso testing. "
         "Is there a method labeled with @Before? If true, save this method to output "
         "before_method and keep the annotation @Before."
         "Also, please save the method annotated with @Test to output test_method and keep the annotation @Test."
         "What is the name of the method that annotated with @Test? \n"
         "%s" % raw_file)

    return get_response_from_gpt(user_prompt, BaseTestMethodGPT)


def base_test_method_build_request_handler(gpt_response_content: str) -> TestMethod:
    """
    Handle the gpt response for test_method_build_request
    :param gpt_response_content:
    :return:
    """
    # convert gpt response to json
    response_json = json.loads(gpt_response_content.strip())

    # initialize a TestMethod
    test_method: TestMethod = TestMethod()

    # get method name
    method_name: str = response_json.get("test_method_name")
    test_method.set_method_name(method_name)

    # set before method attributes
    has_before: bool = response_json.get("has_before_method")
    if has_before:
        before_method_str: str = response_json.get("before_method")
        test_method.set_before_method_str(before_method_str)

    # set test method
    test_method_str: str = response_json.get("test_method")
    test_method.set_method_str(test_method_str)

    return test_method


def build_base_test_info(raw_file: str) \
        -> tuple[TestMethod, list[TestAssertion], list[TestEvent]]:
    """
    This method build a list of Test Assertion and a list of Test Events for original method.
    And these object will be used for further processing of correlation prediction.

    :param raw_file: the original java test method in string
    :return: a list of Test Assertion and a list of Test Events
    """
    # get gpt-response content for method as a whole
    result_raw = base_test_method_build_request(raw_file)
    # handle response for statements
    method = base_test_method_build_request_handler(result_raw)

    # get gpt-response content for statements based on test method
    # extract all assertion and test event starting with onView
    assertions, events = base_test_statements_build_request(method.get_method_str())

    return method, assertions, events
