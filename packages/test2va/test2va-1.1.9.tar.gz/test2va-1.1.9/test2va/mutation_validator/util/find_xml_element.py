import os
import time
import xml.etree.ElementTree as ET

from appium.webdriver import WebElement
from appium.webdriver.webdriver import WebDriver

from ..mappings.maps import WebElementMap
from ..structs.EspressoMatchTypes import EspressoMatchTypes
from ..util.build_xpath_from_element import build_xpath_from_element
from ...parser.structs import XMLElement
from ...parser.types.LibTypes import SelectorData
from ...parser.types.NewGrammar import MatcherData, AssertionData
from ...parser.util.traverse_elements import traverse_elements
from ...util.camel_to_snake import camel_to_snake

# seconds
timeout = 5


def find_xml_element(driver: WebDriver, selector: MatcherData | AssertionData, root=None):
    """Finds an XML element that matches the given selector criteria.

    This function extracts the page source from the driver, converts it to an XML tree,
    and searches for a matching element using defined criteria.

    Args:
        driver (WebDriver): The Appium WebDriver instance.
        selector (MatcherData | AssertionData): A selector defining matching criteria.
        root (WebElement, optional): If provided, searches for elements within this root element.

    Returns:
        tuple[XMLElement | None, str | None, int | None]:
            - The matched `XMLElement` if found, otherwise `None`.
            - The XPath of the matched element, or `None` if not found.
            - The total number of descendant elements in the search scope.
    """
    start = time.time()
    cur = time.time()
    match = None
    while cur - start < timeout:
        # print(match)
        # Get the current page source as XML.
        current_page_src = driver.page_source  # get_static_page_source(driver)

        # Library to find the right criteria mapping.
        library = "Espresso"

        target_map = WebElementMap[library]

        # Write the XML file, so it can be traversed and analyzed.
        with open("temp.xml", "w", encoding="utf-8") as f:
            f.write(current_page_src)

        tree = ET.parse("temp.xml")
        if root is None:
            search_root = traverse_elements(tree.getroot())
        else:
            xml_root = tree.getroot()
            matched_xml_element = find_xml_element_from_webelement(driver, root, xml_root)
            if matched_xml_element is None:
                raise ValueError("The provided WebElement does not correspond to any element in the page source.")
            search_root = traverse_elements(matched_xml_element)

        # Matching functions.
        functions = []
        for criteria in selector["Components"]:
            func_name = camel_to_snake(criteria["Name"])

            if func_name == "has_descendant" and root is not None:
                func = getattr(target_map, "has_descendant_spec")(criteria["Args"], driver, search_root)
            else:
                func = getattr(target_map, func_name)(criteria["Args"], driver, search_root)
            functions.append(func)

        match_type = selector["MatchType"]
        match_type_func = getattr(EspressoMatchTypes, match_type)(functions)

        # Execute the matching functions.
        """def exe(e: XMLElement) -> bool:
            for func in functions:
                if not func(e):
                    return False

            return True"""

        element = search_root.find_first_descendant(lambda e: match_type_func(e))

        if element is not None:
            # This can be flaky because it may find a match in motion from transitions. Meaning, the bounds will be off.
            # The bounds cannot be left out because they are important to discriminate between similar elements.
            # So, we will have to keep checking until the element is static.
            xpath = build_xpath_from_element(element)
            if match is None:
                cur = time.time()
                match = xpath
            elif match == xpath:
                os.remove("temp.xml")
                return element, xpath, len(search_root.find_descendants(lambda e: True))
            else:
                cur = time.time()
                match = xpath
        else:
            cur = time.time()

        time.sleep(0.1)

    os.remove("temp.xml")

    return None, None, None


def find_xml_element_from_webelement(driver: WebDriver, web_element: WebElement, xml_root: ET.Element) -> ET.Element:
    """Finds an XML element in the page source corresponding to the given WebElement.

    This function matches attributes of a `WebElement` against elements in the XML tree
    to find the corresponding representation in the page source.

    Args:
        driver (WebDriver): The Appium WebDriver instance.
        web_element (WebElement): The WebElement to locate in the XML.
        xml_root (ET.Element): The root element of the XML page source.

    Returns:
        ET.Element | None: The matched XML element if found, otherwise `None`.

    Raises:
        ValueError: If the WebElement lacks any identifiable attributes.
    """
    # List of attributes to consider for matching. Adjust as needed.
    attributes_to_check = ["resource-id", "content-desc", "text", "class"]

    # Gather the attributes from the WebElement.
    element_attributes = {}
    for attr in attributes_to_check:
        value = web_element.get_attribute(attr)
        if value:
            element_attributes[attr] = value

    if not element_attributes:
        raise ValueError("The WebElement does not have any of the expected attributes for matching.")

    # Traverse the XML tree to find the matching element.
    for elem in xml_root.iter():
        match = True
        for attr, value in element_attributes.items():
            if elem.get(attr) != value:
                match = False
                break
        if match:
            return elem

    # If no matching element is found, return None.
    return None
