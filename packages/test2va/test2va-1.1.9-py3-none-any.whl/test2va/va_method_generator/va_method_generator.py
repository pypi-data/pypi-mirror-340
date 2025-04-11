import os

from test2va.va_method_generator.core.method_builder import build_test2va_method
from test2va.va_method_generator.core.mutant_report_parser import parser_report_to_events
from test2va.va_method_generator.core.test_script_parser import extract_original_test_method


# TODO: Add an optional argument for srcml xml file then java_file_path is not required
def generate_test2va_method_per_mutant_report(java_file_srcml_path, report_path, output_dir_path):
    method_name, events = parser_report_to_events(report_path)
    old_method_str: str = extract_original_test_method(method_name, java_file_srcml_path)
    method_code_java = build_test2va_method(method_name, events, old_method_str)

    # generate the output path
    output_path = f"{output_dir_path}/{method_name}.java"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(method_code_java)

    return output_path


def generate_all():
    output_folder = os.path.join(os.path.dirname(__file__), "../output")
    examples_folder = os.path.join(os.path.dirname(__file__), "../examples")

    # For each folder in the output folder, verify that the folder contains a file
    # ending in ".java.json" as well as a file called "mutant_data.json".

    for folder in os.listdir(output_folder):
        if folder == ".gitkeep":
            continue

        folder_path = os.path.join(output_folder, folder)

        xml_file = None
        mutant_file = None

        for file in os.listdir(folder_path):
            if file == "java.xml":
                xml_file = os.path.join(folder_path, file)
            elif file == "mutant_data.json":
                mutant_file = os.path.join(folder_path, file)

        if xml_file is None or mutant_file is None:
            print(f"Skipping folder {folder} as it does not contain a java.xml file or mutant_data.json file.")
            continue

        try:
            res = generate_test2va_method_per_mutant_report(xml_file, mutant_file, folder_path)
            # Finally, move res to the output folder
            os.rename(res, os.path.join(folder_path, os.path.basename(res)))
        except Exception as e:
            print(f"Error generating test2va method for {folder}. Error: {e}")
            continue


if __name__ == '__main__':
    generate_all()
    # Code Example of generating a test2va method by mutant report
    # java_file_path = "input/PocketPlan-v.1.4.2_2025-01-21_13-03-38/java.xml"
    # report_path = "input/PocketPlan-v.1.4.2_2025-01-21_13-03-38/mutant_data.json"
    # output_dir_path = "output"
    # generate_test2va_method_per_mutant_report(java_file_path, report_path, output_dir_path)