import re


def camel_to_snake(text: str) -> str:
    """
    Converts a given CamelCase string to snake_case.

    Args:
        text (str): The CamelCase string to convert.

    Returns:
        str: The converted snake_case string.

    Special Cases:
        - If the input text is `"is"`, it returns `"_is"`.
        - If the input text is `"not"`, it returns `"_not"`.

    Example:
        >>> camel_to_snake("CamelCaseExample")
        'camel_case_example'

        >>> camel_to_snake("is")
        '_is'

        >>> camel_to_snake("not")
        '_not'
    """
    if text.lower() == "is":
        return "_is"
    if text.lower() == "not":
        return "_not"
    return re.sub(r'([A-Z])', r'_\1', text).lower()
