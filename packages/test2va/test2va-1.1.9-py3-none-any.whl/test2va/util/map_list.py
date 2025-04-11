from typing import List, Callable

def map_list(lst: List, callback: Callable) -> List:
    """
    Applies a callback function to each element in a list and returns a new list
    with the transformed elements.

    Args:
        lst (List): The list of items to be mapped.
        callback (Callable): A function that takes an item as input and returns a modified item.

    Returns:
        List: A new list containing the transformed items.

    Example:
        >>> numbers = [1, 2, 3, 4, 5]
        >>> square = lambda x: x ** 2
        >>> map_list(numbers, square)
        [1, 4, 9, 16, 25]
    """
    return [callback(item) for item in lst]
