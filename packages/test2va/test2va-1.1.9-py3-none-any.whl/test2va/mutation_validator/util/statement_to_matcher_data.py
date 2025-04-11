import os
import xml.etree.ElementTree as ET

from test2va.parser.new.get_data import get_parse_data
from test2va.parser.types.NewGrammar import MatcherData
from test2va.parser.util.traverse_elements import traverse_elements


def statement_to_matcher_data(state_str: str, assertion=False) -> MatcherData:
    """Converts a Java statement into MatcherData by parsing it with srcML.

    This function creates a temporary Java file with the given statement,
    converts it to XML using `srcml`, and extracts `MatcherData` or assertions
    from the parsed data.

    Args:
        state_str (str): The Java statement to be converted.
        assertion (bool, optional): If `True`, extracts assertion data instead of matchers. Defaults to `False`.

    Returns:
        MatcherData | None: The extracted `MatcherData` or `AssertionData` from the Java statement.
        Returns `None` if parsing fails.
    """
    dummy_file_content = f"@Test\npublic void dummy() {{\n{state_str}\n}}\n"

    # write to file
    with open("dummy.java", "w") as f:
        f.write(dummy_file_content)

    os.system(f'srcml dummy.java -o dummy.xml')

    try:
        tree = ET.parse("dummy.xml")
        root = traverse_elements(tree.getroot())
        data = get_parse_data(root)

        os.remove("dummy.java")
        os.remove("dummy.xml")

        return data[0]["Assertions"][0] if assertion else data[0]["Matchers"][0]
    except Exception as e:
        os.remove("dummy.java")
        os.remove("dummy.xml")
        return None
