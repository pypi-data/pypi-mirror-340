from test2va.bridge.examples import list_examples


def examples_command(_args):
    """Lists available examples.

    Args:
        _args: Command-line arguments (not used in this function).

    Returns:
        None

    Raises:
        None
    """
    examples = list_examples()
    for example in examples:
        print(example)
