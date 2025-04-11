import json, re
from typing import Tuple, Optional

from pydantic import BaseModel

from test2va.va_method_generator.util.gpt_util import get_response_from_gpt
from test2va.va_method_generator.util.util import list_to_str


class Parameter:
    def __init__(self, name: str, param_type: str, possible_values: list = None, is_predefined: bool = False):
        """
        Initializes a Parameter instance.

        :param name: The name of the parameter.
        :param param_type: The type of the parameter.
        :param possible_values: A list of possible values for the parameter.
        :param is_predefined: A boolean indicating whether the parameter has predefined values.
        """
        self.__name = name
        self.__original_value = None
        self.__param_type = param_type
        self.__possible_values = possible_values
        self.__is_predefined = is_predefined

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_original_value(self):
        return self.__original_value

    def set_original_value(self, original_value):
        self.__original_value = original_value

    def get_param_type(self):
        return self.__param_type

    def set_param_type(self, param_type):
        self.__param_type = param_type

    def get_possible_values(self):
        return self.__possible_values

    def set_possible_values(self, possible_values):
        self.__possible_values = possible_values

    def get_is_predefined(self):
        return self.__is_predefined

    def set_is_predefined(self, is_predefined):
        self.__is_predefined = is_predefined

    def __str__(self):
        return f"Parameter(Name: {self.__name}, Original Value: {self.__original_value}, Type: {self.__param_type}, Values: {self.__possible_values}, Is Predefined: {self.__is_predefined})"


class Event:
    def __init__(self, original_statement: str, is_mutable: bool):
        """
        Initializes an Event instance.

        :param original_statement: The original statement as a string.
        :param is_mutable: A boolean indicating whether the event is mutable.
        """
        self.__original_statement: str = original_statement
        self.__is_mutable: bool = is_mutable
        self.__parameter: Parameter = None
        self.__mutant_statements: list[str] = []

    def __str__(self):
        """Returns a formatted string representation of the event."""
        mutant_str = "\n    ".join(self.__mutant_statements) if self.__mutant_statements else "None"
        param_str = str(self.__parameter) if self.__parameter else "None"
        return f"Original Statement: {self.__original_statement}\nIs Mutable: {self.__is_mutable}\nParameter:\n    {param_str}\nMutant Events:\n    {mutant_str}\n"

    def get_original_statement(self) -> str:
        """Returns the original statement of the event."""
        return self.__original_statement

    def get_mutant_statements(self) -> list[str]:
        """Returns the list of mutant events."""
        return self.__mutant_statements

    def is_mutable(self) -> bool:
        """Returns whether the event is mutable."""
        return self.__is_mutable

    def set_mutable_to_false(self):
        """
        Set the mutable to False
        """
        self.__is_mutable = False

    def add_mutant_statement(self, mutant_statement: str):
        """Adds a mutant event to the event."""
        self.__mutant_statements.append(mutant_statement)

    def get_parameter(self) -> Parameter:
        """Returns the parameter object."""
        return self.__parameter

    def set_parameter(self, parameter: Parameter):
        """Sets the parameter object."""
        self.__parameter = parameter


def collect_test_method_name(file_path):
    """
    Collects the test method name from the first non-empty item in the JSON
    file, considering only integer keys.

    :param file_path: The mutant report path
    :return: The extracted method name, or None if no valid method is found.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter keys that are integers and sort them
    int_keys = sorted((int(k) for k in data if k.isdigit()), key=int)

    for key in int_keys:
        if data[str(key)]:  # Ensure the item is not empty
            method_name = data[str(key)]['test_method_name']
            return method_name
    return None


def collect_events(file_path):
    """
    Builds a list of Event objects from the JSON file, considering only integer keys.

    :param file_path: Path to the JSON file.
    :return: A list of Event objects.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    events = []

    # Filter keys that are integers and sort them
    int_keys = sorted((int(k) for k in data if k.isdigit()), key=int)

    for key in int_keys:
        item = data[str(key)]  # Ensure accessing the correct key as JSON stores them as strings
        original_statement: str = item.get('statement', "")
        is_mutable = item.get('is_mutable', False)
        event_obj = Event(original_statement, is_mutable)

        for mutant in item.get('mutant_events', []):
            mutant_statement: str = mutant.get('statement', "")
            if mutant_statement.lower() != original_statement.lower():  # Only add if different
                event_obj.add_mutant_statement(mutant_statement)

        events.append(event_obj)

    return events


def extract_innermost_values(statement):
    """
    Extracts values from the innermost pairs of parentheses in the given statement.
    :param statement: The input string containing nested function calls.
    :return: A list of extracted values.
    """
    matches = re.findall(r'\(([^()]+)\)', statement)
    return matches


# TODO: now the algorithm only works with only one difference
def find_different_index(original_list, mutant_lists):
    """
    Finds the index where the elements in mutant_lists differ from original_list.
    :param original_list: (list) The reference list to compare against.:
    :param mutant_lists: (list of list) A list of lists to compare with the original.
    :return: The index where the first difference occurs, or -1 if no differences.

    Example:
        original_list = ['R.id.theme', '"Light"']
        mutant_lists = [
            ['R.id.theme', '"Dark"'],
            ['R.id.theme', '"Default"']
        ]
        find_different_index(original_list, mutant_lists)  # Output: 1

        original_list = ['R.id.theme1', '"Light"']
        mutant_lists = [
            ['R.id.theme2', '"Light"'],
            ['R.id.theme3', '"Light"']
        ]
        find_different_index(original_list, mutant_lists)  # Output: 0

        original_list = ['R.id.theme', '"Light"']
        mutant_lists = [
            ['R.id.theme', '"Light"'],
            ['R.id.theme', '"Light"']
        ]
        find_different_index(original_list, mutant_lists)  # Output: -1

    """
    for i in range(len(original_list)):
        original_value = original_list[i]

        # Check if any of the mutant lists have a different value at index i
        if any(mutant[i] != original_value for mutant in mutant_lists):
            return i  # Return the first differing index

    return -1  # Return -1 if no differences are found


def find_values_from_statements(original_statement, mutant_statements) -> Tuple[Optional[str], Optional[list[str]]]:
    """
    Find the original value and the mutant values by comparing the original statement and the mutant statements.
    :param original_statement: The original statement to compare.
    :param mutant_statements: A list of mutant statements to compare against.
    :return: Tuple[Optional[str], Optional[List[str]]]: A tuple containing the original differing value and a list of
        possible mutant values. Returns (None, None) if no differences are found.
    """

    # collect the value lists
    original_value_list = extract_innermost_values(original_statement)
    mutant_values_lists = []
    for stmt in mutant_statements:
        mutant_values_lists.append(extract_innermost_values(stmt))

    # find the different value's index in original list
    diff_index: int = find_different_index(original_value_list, mutant_values_lists)

    if diff_index == -1:
        return None, None  # No difference found

    original_value: str = original_value_list[diff_index]
    possible_values: list[str] = []
    for mutant_values in mutant_values_lists:
        possible_values.append(mutant_values[diff_index])

    return original_value, possible_values


class ReplacedDecision(BaseModel):
    by_user: bool
    by_developer: bool


def collect_is_predefined_from_ai(user_prompt):
    """
    Collect the AI model decision about if the values are decide by user or developers
    :param user_prompt: gpt prompt
    :return: is_pre_defined decision, True or False
    """

    gpt_response = get_response_from_gpt(user_prompt, ReplacedDecision)
    response_json = json.loads(gpt_response.strip())

    if response_json.get("by_developer") and not response_json.get("by_user"):
        is_pre_defined = True
    elif response_json.get("by_user") and not response_json.get("by_developer"):
        is_pre_defined = False
    else:
        raise PreDefinedDecisionUndeterminedException(f"the pre_defined cannot be decided for statement.")

    return is_pre_defined


# TODO: Can only handle one different part per statement
def is_input_parameter(original_statement: str) -> bool:
    """Detects if an Espresso statement contains typeText(X) or replaceText(X)."""
    return bool(re.search(r'\.perform\((typeText|replaceText)\(.*?\)\)', original_statement))


def collect_parameter_info(method_name: str, original_statement: str, mutant_statements: list[str]) \
        -> Tuple[str | None, bool, list[str] | None]:
    original_value, possible_values = find_values_from_statements(original_statement, mutant_statements)
    if original_value is None and possible_values is None:
        print("No differences found")
        return None, False, None

    if is_input_parameter(original_statement):
        is_pre_defined = False
    else:
        # prepare the is_predefined query
        user_prompt \
            = ("In an espresso test method named %s, "
               "Compare the statements below: \n"
               "%s\n"
               "%s\n"
               "You will see these statements have the different values of:\n%s\n%s."
               "Do these values defined by app developer or create by app users? Only choose one, no explain."
               % (
                   method_name, original_statement, list_to_str(mutant_statements), original_value,
                   list_to_str(possible_values)))

        is_pre_defined = collect_is_predefined_from_ai(user_prompt)

    return original_value, is_pre_defined, possible_values


def update_parameters(method_name: str, events: list[Event]) -> list[Event]:
    """
    Updates parameters by creating a Parameter object for mutable events.
    :param method_name: method name for the test2va service
    :param events: the list of events that apply
    :return: a list with event with parameters updated
    """
    """"""
    for index, event in enumerate(events):

        # update the event, double check the is_mutable feature
        if len(event.get_mutant_statements()) == 0:
            event.set_mutable_to_false()

        if event.is_mutable():
            print(f"update parameter in event: {event.get_original_statement()}")

            # 1. collect name
            param_name = f"param{index}"
            # 2. collect type
            param_type = "String"
            # 3. collect the parameter pre-defined value
            origin_statement = event.get_original_statement()
            mutant_statements = event.get_mutant_statements()

            origin_value, is_pre_defined, possible_values \
                = collect_parameter_info(method_name, origin_statement, mutant_statements)

            # 4. build the parameter of this statement
            param: Parameter = Parameter(param_name, param_type, possible_values, is_pre_defined)
            param.set_original_value(origin_value)

            # 5. add parameter back to event
            event.set_parameter(param)

    return events


def convert_to_test2va_method_name(test_method_name: str) -> str:
    """
    Removes the last occurrence of 'Test' (case-insensitive) from original method name
    :param test_method_name: original name
    :return:
    """
    if test_method_name.lower().endswith("test"):
        method_name = test_method_name[:-4]  # Remove the last 'Test'
        return method_name


def parser_report_to_events(report_path: str) -> Tuple[str, list[Event]]:
    """
    Parse the mutant report file to generate the method name and the a list of events
    :param report_path: the file path of mutant report
    :return:
    """
    # collect original test method name.
    test_method_name: str = collect_test_method_name(report_path)
    # convert to the new name
    method_name = convert_to_test2va_method_name(test_method_name)
    # collect statements
    events: list[Event] = collect_events(report_path)
    # update the potential parameters in all events
    events = update_parameters(method_name, events)

    print("parser_report_to_events is finished.")

    return method_name, events


if __name__ == '__main__':
    # test Example usage:
    file_path = "../input/addNewFood/mutant_data.json"  # Replace with your actual JSON file path
    name, statements = parser_report_to_events(file_path)

    print(name)
    for stmt in statements:
        print(stmt)
