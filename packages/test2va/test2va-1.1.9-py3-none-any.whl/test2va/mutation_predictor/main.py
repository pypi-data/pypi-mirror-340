import os

from openai import OpenAI

# The GPT_API_KEY is needed for gpt usage
# and APK_LIST is needed for batch analysis
# from test2va.mutation_predictor.config.config import APK_LIST
# from test2va.mutation_predictor.config.gpt_config import GPT_API_KEY


from test2va.mutation_predictor.core.basic_test.base_test_operations import build_base_test_info
from test2va.mutation_predictor.core.events.common_ops import build_mutation_report
from test2va.mutation_predictor.core.events.main import generate_mutant_event_candidates
from test2va.mutation_predictor.util.util import read_file_to_string, save_json_to_file, get_java_test_file_names


def mutant_analysis_per_app(pg_src_path: str, j_path: str, output_path: str):

    # apply the process for each java test method.
    # app_test_method_path: str = f"{test_method_path}{app_apk_name}/"
    # app_test_file_names: list[str] = get_java_test_file_names(app_test_method_path)

    # for test_file_name in app_test_file_names:
    # prep1: define test method path
    test_method_full_path: str = j_path
    print(test_method_full_path)

    # prep2: define xml context path
    # test_method_name = test_file_name[0].lower() + test_file_name[1:]
    xml_content_path: str = pg_src_path
    print(xml_content_path)

    # step1. get the raw test code
    test_method_raw: str = read_file_to_string(test_method_full_path)
    # print(test_method_raw)

    # step2. build the base test info.
    method, assertions, events = build_base_test_info(test_method_raw)

    # step3. collect the mutant event
    events = generate_mutant_event_candidates(assertions, events, xml_content_path, method)

    # step4. build the report
    mutation_report: dict = build_mutation_report(events)

    # step5. write the report as json file to output path
    j_file_name = os.path.basename(test_method_full_path)
    analysis_output_full_path = f"{output_path}/{j_file_name}.json"
    save_json_to_file(mutation_report, analysis_output_full_path)

    return mutation_report


def analysis_start(pg_src_path: str, j_path: str, output_path: str):
    # test_method_path = "test_methods/"
    # analysis_output_path = "mutant_prediction_report/"

    # conduct the analysis for each app
    # for apk_name in APK_LIST:
    return mutant_analysis_per_app(pg_src_path, j_path, output_path)


# TODO: reorganize the input and output
def mutant_analysis_per_app_per_test(file_path, xml_context_path, output_path):
    # get the method
    # file_path = 'test_methods/another-notes-app-1.5.4/SearchingNoteTest.java'
    # xml_context_path = 'test_methods/another-notes-app-1.5.4/xml-content/searchingNoteTest'
    # output_path = 'mutant_prediction_report/another-notes-app-1.5.4/SearchingNoteTest.java.json'

    # step1. get the raw test code
    test_method_raw: str = read_file_to_string(file_path)
    # print(test_method_raw)

    # step2. build the base test info.
    method, assertions, events = build_base_test_info(test_method_raw)

    # step3. collect the mutant event
    events = generate_mutant_event_candidates(assertions, events, xml_context_path, method)

    # step4. build the report
    mutation_report: dict = build_mutation_report(events)

    # step5. write the report as json file to output path
    save_json_to_file(mutation_report, output_path)


if __name__ == '__main__':

    # analysis_start()
    file_path = '../test/medTimer/DeleteMedicineTest/DeleteMedicineTest.java'
    xml_context_path = '../test/medTimer/DeleteMedicineTest/pg_src'
    output_path = '../test/medTimer/DeleteMedicineTest/DeleteMedicineTest.java.json'
    mutant_analysis_per_app_per_test(file_path, xml_context_path, output_path)