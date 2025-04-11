import re
import subprocess
import os
import shutil
import lxml.etree as ET

from test2va.va_method_generator.util.util import read_file_to_string

#TODO: add install requirement for lxml, also check the srcml


def check_srcml():
    """
    Checks if srcML is installed and available in the system PATH.
    """
    if not shutil.which("srcml"):
        print("Error: srcML is not installed or not found in the system PATH.")
        print("Please install srcML from https://www.srcml.org/ and ensure it's accessible in your terminal.")
        return False
    return True

def srcml_convert_java_to_xml(java_path, xml_path):
    """
    Converts a Java file to an XML file using srcML.

    :param java_path: Path to the Java source file.
    :param xml_path: Path to save the converted XML file.
    """
    if not os.path.exists(java_path):
        raise FileNotFoundError(f"Java file not found: {java_path}")

    # Check if srcML is available in the system path
    if not check_srcml():
        return

    try:
        # Run the srcML command
        # result = subprocess.run(["pwd"], capture_output=True, text=True)
        # print(result.stdout.strip())

        os.system(f'srcml "{java_path}" -o {xml_path}')
        print(f"Conversion successful: {xml_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting Java to XML: {e}")


def srcml_extract_method_from_xml(xml_path, method_name, output_xml_path):
    """
    Extracts a specific method from an XML file using srcML.

    :param xml_path: Path to the XML file.
    :param method_name: Name of the method to extract.
    :param output_xml_path: Path to save the extracted method in XML format.
    """
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    try:
        # Parse XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Define srcML namespace
        ns = {'src': 'http://www.srcML.org/srcML/src'}

        # XPath query to find the function by name
        xpath_query = f"//src:function[src:name='{method_name}Test']"
        method_element = root.xpath(xpath_query, namespaces=ns)

        if method_element:
            # Create new XML tree with only the extracted method
            new_root = ET.Element("unit", nsmap={"src": "http://www.srcML.org/srcML/src"})
            new_root.append(method_element[0])

            # Write extracted function to a new XML file
            new_tree = ET.ElementTree(new_root)
            new_tree.write(output_xml_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

            print(f"Method '{method_name}' extracted successfully to: {output_xml_path}")
        else:
            print(f"Method '{method_name}' not found in XML file.")

    except ET.XMLSyntaxError as e:
        print(f"Error parsing XML file: {e}")


def srcml_convert_xml_to_java(xml_path, java_path):
    """
    Converts an XML file back to a Java file using srcML.

    :param xml_path: Path to the XML file.
    :param java_path: Path to save the converted Java file.
    """
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    # Check if srcML is available in the system path
    if not check_srcml():
        return

    try:
        # Run the srcML command to convert XML back to Java
        # Use --language=Java to specify the output format
        os.system(f'srcml --language=Java "{xml_path}" -o "{java_path}"')
        print(f"Conversion to Java successful: {java_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting XML to Java: {e}")


def extract_original_test_statements(method_name, file_path):
    """
    Extracts all the statements inside a Java test method annotated with @Test.

    :param method_name: Name of the Java test method (e.g., "checkShoppingItemTest")
    :param file_path: Path to the Java test file
    :return: List of extracted statements inside the method
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    is_test = False  # Flag to check if the method is a @Test method
    inside_method = False  # Flag to check if we are inside the method body
    brace_stack = []  # Stack to track opening and closing braces
    statements = []

    for line in lines:
        stripped_line = line.strip()

        # Flag @Test annotation
        if stripped_line == "@Test":
            is_test = True
            continue  # Move to next line

        # If @Test was found, check for method signature
        if is_test and re.match(rf"public\s+void\s+{method_name}\s*\(.*\)\s*(?:throws\s+\w+)?\s*{{", stripped_line):
            inside_method = True
            brace_stack.append("{")  # Push first opening brace onto the stack
            continue  # Move to next line

        # If inside the method, track braces and extract statements
        if inside_method:
            # Count opening and closing braces in the line
            open_brace_count = stripped_line.count("{")
            close_brace_count = stripped_line.count("}")

            # Push all `{` found in the line onto the stack
            for _ in range(open_brace_count):
                brace_stack.append("{")

            # Append the statement **before** checking for closing braces
            statements.append(stripped_line)

            # Pop all `}` from the stack and check if the method ends
            for _ in range(close_brace_count):
                if brace_stack:
                    brace_stack.pop()
                if not brace_stack:  # Stack is empty, method has ended
                    return statements  # Return immediately after last statement

    return statements if statements else f"Error: Method '{method_name}' not found or has no statements."


def reformat_java_method(java_code):
    """
    Automatically reformats a Java test method by:
    - Removing annotations like @Test
    - Removing unnecessary newlines while maintaining readability
    - Keeping indentation intact

    :param java_code: The original Java method as a string.
    :return: The reformatted Java method as a string.
    """
    # 1. Remove @Test annotation (or any annotation starting with @)
    java_code = re.sub(r"@\w+\s*\n", "", java_code)

    # 2. Remove all new lines inside the method while keeping proper structure
    java_code = re.sub(r"\n\s*", " ", java_code)  # Remove unnecessary newlines while keeping spaces

    # 3. Remove last extra closing brace "}" if it exists
    java_code = java_code.strip()
    if java_code.endswith("}"):
        java_code = java_code[:-1].strip()

    # 4. Insert a newline after "{"
    java_code = re.sub(r"\{\s*", "{\n", java_code)

    # 5. Insert a newline after ";"
    java_code = re.sub(r";\s*", ";\n", java_code)

    # fix ")." → Ensures there’s no space before .perform(click());
    java_code = re.sub(r"\)\s+\.", ").", java_code)

    # 5. Add indentation (4 spaces) for each statement
    formatted_lines = []
    for line in java_code.splitlines():
        if line.endswith(";"):  # this line is a statement
            formatted_lines.append("    " + line)
        else:
            formatted_lines.append(line)

    # Join and return the final formatted method
    return "\n".join(formatted_lines)


def extract_original_test_method(test_method_name, class_xml_file) -> str:
    """
    Using srcml to extract the test method as a whole string
    :param test_method_name: test method name
    :param class_xml_file: test class file path
    :return: the test method as a string
    """

    # 1) Get the directory of the Java file
    directory = os.path.dirname(class_xml_file)
    print("Directory:", directory)

    # 2) Create a new file path for method extraction
    extracted_method_java_path = os.path.join(directory, f"method_{test_method_name}.java")

    # # If temp_process_files directory does not exist, create it
    # temp_path = os.path.join(os.path.dirname(__file__), "../temp_process_files")
    # if not os.path.exists(temp_path):
    #     os.makedirs(temp_path)

    method_xml_file = os.path.join(directory, f"method.srcml.xml")  # XML output path

    # Extract the method
    srcml_extract_method_from_xml(class_xml_file, test_method_name, method_xml_file)

    # Convert the extracted method back to Java
    srcml_convert_xml_to_java(method_xml_file, extracted_method_java_path)

    # reformat the extracted method
    reformatted_java_code = reformat_java_method(read_file_to_string(extracted_method_java_path))

    return reformatted_java_code


if __name__ == '__main__':
    # Example usage

    java_file = "../input/test/AddShoppingItemTest.java"  # Replace with your Java file path
    method_name = "addShoppingItemTest"  # Replace with the method name you want to extract

    original_test_method_code = extract_original_test_method(method_name, java_file)

    # Print the reformatted output
    print(original_test_method_code)
