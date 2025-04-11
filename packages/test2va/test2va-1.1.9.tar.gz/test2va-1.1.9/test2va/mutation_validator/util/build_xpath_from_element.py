def build_xpath_from_element(element):
    """Constructs an XPath expression from an XML element's attributes.

    Args:
        element (xml.etree.ElementTree.Element): The XML element from which to build the XPath.

    Returns:
        str: An XPath string that uniquely identifies the element based on its attributes.
    """
    xpath_parts = []

    for attr, value in element.attrib.items():
        # Skip empty attributes or attributes with special characters
        if not value or " " in value or attr in {"checked", "selected"}:
            continue

        xpath_parts.append(f"@{attr}='{value}'")

    xpath = f"//{element.tag}[" + " and ".join(xpath_parts) + "]"
    return xpath
