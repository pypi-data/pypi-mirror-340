from typing import List, Callable

def filter_list(lst: List, callback: Callable) -> List:
    """
    Filters a list based on a given callback function.

    Args:
        lst (List): The list to be filtered.
        callback (Callable): A function that takes an item as input
            and returns `True` if the item should be included, otherwise `False`.

    Returns:
        List: A new list containing only the items for which the callback function returned `True`.

    Example:
        >>> numbers = [1, 2, 3, 4, 5]
        >>> is_even = lambda x: x % 2 == 0
        >>> filter_list(numbers, is_even)
        [2, 4]
    """
    filtered_list = [item for item in lst if callback(item)]
    return filtered_list
