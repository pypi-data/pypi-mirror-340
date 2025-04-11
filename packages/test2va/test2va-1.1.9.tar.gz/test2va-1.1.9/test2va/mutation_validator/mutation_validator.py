import time
from threading import Thread, Event
from appium.webdriver.webdriver import WebDriver
from selenium.common import InvalidElementStateException

from test2va.mutation_predictor.main import analysis_start
from test2va.mutation_predictor.util.util import save_json_to_file
from test2va.mutation_validator.util.clear_user_data import clear_user_data

from test2va.mutation_validator.util.execute_action import execute_action
from test2va.mutation_validator.util.execute_assertion import execute_assertion
from test2va.mutation_validator.util.find_ele_xpath_fallback import find_ele_xpath_fallback
from test2va.mutation_validator.util.grant_permissions import grant_permissions
from test2va.mutation_validator.util.setup_test import setup_test
from test2va.mutation_validator.util.statement_to_matcher_data import statement_to_matcher_data

from test2va.parser.types.NewGrammar import ParseData

"""
Data Input Example (ai_data):
{
"0": {
        "is_mutable": false,
        "statement": "onView(allOf(withContentDescription(\"Open drawer\"), isDisplayed())).perform(click());",
        "xpath": "//android.widget.ImageButton[@index='0' and @class='android.widget.ImageButton' and @checked='false' and @package='com.maltaisn.notes.sync' and @content-desc='Open drawer']",
        "mutant_events": [],
        "test_method_name": "createLabelTest"
    },
"1": {
        "is_mutable": true,
        "statement": "onView(allOf(withText(\"Create new label\"), isDisplayed())).perform(click());",
        "xpath": "//android.widget.CheckedTextView[@index='0' and @text='Create new label' and @resource-id='com.maltaisn.notes.sync:id/design_menu_item_text' and @checked='false' and @package='com.maltaisn.notes.sync']",
        "mutant_events": [
            {
                "origin_event_index": 1,
                "statement": "onView(allOf(withText(\"Notes\"), isDisplayed())).perform(click());",
                "xpath": "//android.widget.CheckedTextView[@index='0' and @text='Notes' and @resource-id='com.maltaisn.notes.sync:id/design_menu_item_text' and @checked='true' and @package='com.maltaisn.notes.sync']",
                "assertion_statement": ""
            },
        ...
}
"""

# TODO: Teardown?
# TODO: Modify AI report and send examples
# TODO: Fill out spreadsheet https://villanova-my.sharepoint.com/:x:/r/personal/xqin_villanova_edu/_layouts/15/Doc.aspx?sourcedoc=%7B33BBA5BA-49A7-4C2B-9E1E-31CE8A53F74C%7D&file=stats.xlsx&action=default&mobileredirect=true
# TODO: AI only button / button for each step
# TODO: AI result caching for repeat tests
# TODO: CLI ai support
# TODO: GUI ai logging indication


def mutation_validator(driver: WebDriver, p_data: ParseData, ai_data, output_path: str, auto_grant_perms):
    app_id = driver.current_package

    # TODO: Teardown?

    # Loop through each entry in ai_data
    for key, value in ai_data.items():
        event_index = key

        # If this step is not mutable, just skip it
        if not value["is_mutable"]:
            continue

        actually_mutable = []

        # For each mutant event in this step
        for mutant_event in value["mutant_events"]:
            # First, reset and clear user data.
            driver.terminate_app(app_id)
            clear_user_data(driver, app_id)
            grant_permissions(driver, app_id, auto_grant_perms)
            driver.activate_app(app_id)

            # Set up the test
            if p_data["Before"] is not None:
                setup_test(driver, p_data, True)

            early_exit = False
            actually_mutable.append(mutant_event)

            # For each step in the test
            for idx, step in enumerate(p_data["Matchers"]):
                # By default, execute as base step
                matcher_data = step
                target_xpath = ai_data[idx]["xpath"]

                # If index is the current step being mutated, execute as mutated event instead
                if idx == event_index:
                    matcher_data = statement_to_matcher_data(mutant_event["statement"])
                    target_xpath = mutant_event["xpath"]

                if matcher_data is None:
                    print(f"Event {event_index} proposed mutable event index statement {mutant_event['statement']} was not actually mutable.")
                    early_exit = True
                    break

                # Otherwise, continue as a base step
                web_element, final_xpath = find_ele_xpath_fallback(driver, target_xpath, matcher_data)

                if web_element is None:
                    # If it couldn't find the element, then this must not be a valid mutation
                    print(
                        f"Event {event_index} proposed mutable event index statement {mutant_event['statement']} was "
                        f"not actually mutable."
                    )
                    early_exit = True
                    break

                # If it found the element, then execute the action
                try:
                    execute_action(driver, web_element, final_xpath, matcher_data["Action"])
                except InvalidElementStateException as e:
                    print(
                        f"Event {event_index} proposed mutable event index statement {mutant_event['statement']} was "
                        f"not actually mutable."
                    )
                    early_exit = True
                    break

            # Assert
            if early_exit:
                # Pop from actually_mutable
                actually_mutable.pop()
                continue

            assertions = p_data["Assertions"]

            # Loop through each assertion
            assertion_results = []
            for idx, assertion in enumerate(assertions):
                target = assertion

                # If this particular assertion needed to be mutated
                if str(idx) in mutant_event["assertion_statement"]:
                    target = statement_to_matcher_data(mutant_event["assertion_statement"][str(idx)], True)

                passed = execute_assertion(driver, [target])
                assertion_results.append(passed)

                if not passed:
                    print(f"Event {event_index} proposed mutable event index statement {mutant_event['statement']} failed.")
                    break

            if not all(assertion_results):
                # Pop from actually_mutable
                actually_mutable.pop()
                continue

            # TODO: Teardown?

        value["mutant_events"] = actually_mutable

        if len(value["mutant_events"]) == 0:
            value["is_mutable"] = False

    return ai_data
