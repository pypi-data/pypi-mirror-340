from test2va.bridge import get_stats
from test2va.bridge.stats import get_stat_string


def stats_list_command():
    """Lists all available statistics.

    Retrieves available statistics and prints them in a numbered list.

    Returns:
        None
    """
    stats = get_stats()

    if len(stats) == 0:
        print("No statistics available.")
        return

    for i, stat in enumerate(stats, start=1):
        print(f"{i}. {stat['name']}")


def stats_view_command(index):
    """Displays detailed information about a specific statistic.

    Args:
        index (int): The index of the statistic to view.

    Returns:
        None
    """
    print(get_stat_string(index))
