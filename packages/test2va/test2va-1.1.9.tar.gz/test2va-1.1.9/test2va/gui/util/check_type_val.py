
# Val is always a string.
# Return true or false
def check_type_val(type, val):
    """Checks if the given value matches the expected type.

    Args:
        type (str): The expected type of the value ("str", "int", or "bool").
        val (str): The value to be checked, always passed as a string.

    Returns:
        bool: True if the value matches the expected type, False otherwise.
    """
    if type == "str":
        return True
    elif type == "int":
        try:
            int(val)
            return True
        except ValueError:
            return False
    elif type == "bool":
        return val.lower() == "true" or val.lower() == "false"

