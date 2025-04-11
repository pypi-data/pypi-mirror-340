from pydantic import BaseModel
import json

from test2va.mutation_predictor.util.util import read_file_to_string
from test2va.mutation_predictor.util.gpt_util import get_response_from_gpt


class ElementMutatorGPT(BaseModel):
    original_node: str
    original_statement: str
    class_attribute_value: str
    qualified_nodes: list[str]
    modified_statements: list[str]


class ElementMutator:

    @staticmethod
    def collect_element_mutants(statement: str, full_xml_context_path: str):
        user_prompt = \
            ("Which original node in the below xml tree does the statement: \"%s\" represents? "
             "What is the value of this original node's class attribute?"
             "Among all the rest node in this tree, what are all the qualified nodes with same depth of this original node"
             " and have the same value of class attribute? "
             "If I want to replace the original with each of the qualified nodes, how can I modify the statement? "
             "Please only update the argument values in this statement, do not add any new arguments. No explain.\n"
             "%s"
             % (statement, read_file_to_string(full_xml_context_path)))

        gpt_response = get_response_from_gpt(user_prompt, ElementMutatorGPT)

        response_json = json.loads(gpt_response.strip())

        return (response_json.get("original_node"), response_json.get("qualified_nodes"),
                response_json.get("modified_statements"))

