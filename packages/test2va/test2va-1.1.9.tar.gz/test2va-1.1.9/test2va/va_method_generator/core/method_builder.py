import re
from typing import Tuple

from test2va.va_method_generator.core.convert_espresso_to_test2va import convert_espresso_statement, validate_non_espresso_statement
from test2va.va_method_generator.core.mutant_report_parser import Event, Parameter, parser_report_to_events
from test2va.va_method_generator.exceptions.exceptions import UnsupportedEventException, UnsupportedNonEspressoStatementException, \
    IllegalMethodFormatException


def generate_test2va_statement(event: Event) -> Tuple[str, Parameter|None]:
    """
    Generate the test2va statement from the event
    :param event:
    :return:
    """
    test2va_statement: str = ""
    parameter: Parameter = None

    if not event.is_mutable() and event.get_parameter() is None:  # no mutant, no parameter
        espresso_statement = event.get_original_statement()
        test2va_statement = convert_espresso_statement(espresso_statement)
    elif event.is_mutable() and event.get_parameter() is not None:  # has mutant, has parameter
        parameter = event.get_parameter()
        if not parameter.get_is_predefined():  # no pre-defined value
            original_value = parameter.get_original_value()
            param_name = parameter.get_name()
            espresso_statement = event.get_original_statement().replace(original_value, param_name)
            test2va_statement = convert_espresso_statement(espresso_statement)
        else:
            test2va_statement = generate_java_if_statement(event.get_original_statement(), parameter)
    else:  # has pre-defined values
        raise UnsupportedEventException(event)

    return test2va_statement, parameter


def build_test2va_method(method_name: str, event_list: list[Event], old_method: str) -> str:
    """
    Generates a Java method based on the mutant report event list and the original test method
    :param old_method: The string representation of the old method
    :param method_name: original method name
    :param event_list: the event in the method
    :return:
    """

    new_statements_list = []  # Store Java style test2va statements
    parameter_list = []
    old_method_lines = old_method.splitlines()

    if len(old_method_lines) < 2:
        raise IllegalMethodFormatException(old_method)

    # Step 1. process the method body
    # 1.1 collect the old statements in the method, including the method ending }
    old_statements_list = old_method_lines[1:]
    counter = 0  # counter
    total = len(old_statements_list)  # total number of event

    # 1.2 for all the old statement
    for old_statement in old_statements_list:
        old_statement = re.sub(r"^\s+|\s+$", "", old_statement)  # Trimming Leading and Trailing Spaces
        print(f"convert statement {counter}/{total}: {old_statement} . . . . . .")
        if "onView" not in old_statement:  # is not an espresso statement
            if validate_non_espresso_statement(old_statement):
                new_statements_list.append(f"    {old_statement}")
            elif old_statement == "}":
                new_statements_list.append(f"{old_statement}")
            else:
                raise UnsupportedNonEspressoStatementException(old_statement)

        else:  # is an espresso statement
            is_converted = False  # flag of whether old_statement has been processed.
            for event in event_list:
                # found the mutant event of the old statement,
                if not is_converted and event.get_original_statement() in old_statement:
                    is_converted = True
                    test2va_statement, parameter = generate_test2va_statement(event)

                    if test2va_statement:  # not empty
                        new_statements_list.append(f"    {test2va_statement}")
                    if parameter is not None:  # not None
                        parameter_list.append(parameter)  # Store parameter

                    break

            # the statement is not found in mutation report, mean it is an assertion
            if not is_converted:
                continue

    # Step 2. process the method header
    old_method_head = old_method_lines[0]

    # 2.1 update the method name
    new_method_head = old_method_head.replace(f"{method_name}Test", f"{method_name}")

    # 2.2 insert the parameter list
    param_str = ", ".join(f"{param.get_param_type()} {param.get_name()}" for param in parameter_list)
    new_method_head = new_method_head.replace(f"()", f"({param_str})")

    # Step 3. put the method code together.
    new_method_code = f"{new_method_head}\n"
    new_method_code = new_method_code + "\n".join(new_statements_list)
    new_method_code += "\n"

    print("build_test2va_method is finished.")

    return new_method_code


def to_test2va_id_references(text):
    """
    Converts 'R.id.X' and 'id.X' to '"X"', while keeping other text unchanged.
    :param text: Input string containing references
    :return: Updated string with proper replacements
    """
    return re.sub(r'\b(?:R\.id\.|id\.)(\w+)\b', r'"\1"', text)


def generate_java_if_statement(original_statement: str, parameter: Parameter) -> str:
    """
    Generates a properly formatted Java if-else statement for predefined parameter values.

    :param original_statement: Original Espresso statement.
    :param parameter: The parameter detected for this statement.
    :return: A correctly formatted Java if-else statement.
    """
    param_name = parameter.get_name()
    original_value = parameter.get_original_value()
    possible_values = parameter.get_possible_values()

    # Start with the 'if' condition
    if_statement = f'if ({param_name}.equalsIgnoreCase({to_test2va_id_references(original_value)})) {{\n'
    if_statement += f'        {convert_espresso_statement(original_statement)}\n'

    # Generate 'else if' conditions
    for value in possible_values:
        if_statement += f'    }} else if ({param_name}.equalsIgnoreCase({to_test2va_id_references(value)})) {{\n'
        if_statement += f'        {convert_espresso_statement(original_statement.replace(original_value, value))}\n'

    # Close the final if-else block
    if_statement += "    }"

    return if_statement


if __name__ == '__main__':
    # Test Example usage
    file_path = "../input/addNewFood/mutant_data.json"  # Replace with your actual JSON file path
    name, events = parser_report_to_events(file_path)

    for stmt in events:
        print(stmt)

    print(build_test2va_method(name, events))