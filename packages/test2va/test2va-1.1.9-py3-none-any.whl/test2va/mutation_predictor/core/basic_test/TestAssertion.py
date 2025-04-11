# TestAssertion class
from test2va.mutation_predictor.core.basic_test.TestTypes import AssertionType
from test2va.mutation_predictor.core.basic_test.TestEvent import TestEvent


class TestAssertion:
    def __init__(self, index: int = None, type_: AssertionType = None, statement: str = "",
                 related_events_indices: list[int] = None, test_method_name: str = "",
                 is_value_overlapped: bool = False):
        """
        Initializes the TestAssertion class. Allows empty constructor.

        Args:
            index (int, optional): The index of the assertion. Defaults to None.
            type_ (AssertionType, optional): The type of the assertion (Type1, Type2, Type3). Defaults to None.
            statement (str, optional): The statement associated with the assertion. Defaults to an empty string.
            related_events_indices (list of int, optional): A list of event indices related to this assertion. Defaults to None.
            test_method_name (str, optional): The name of the test method associated with this assertion. Defaults to an empty string.
            is_value_overlapped (bool, optional): Indicates if the value is overlapped. Defaults to False.
        """
        self._index = index
        self._type = type_
        self._statement = statement
        self._related_events_indices = related_events_indices if related_events_indices is not None else []
        self._test_method_name = test_method_name
        self._is_value_overlapped = is_value_overlapped

    # Getter for index
    def get_index(self) -> int:
        return self._index

    # Setter for index
    def set_index(self, index: int):
        self._index = index

    # Getter for type
    def get_type(self) -> AssertionType:
        return self._type

    # Setter for type
    def set_type(self, type_: AssertionType):
        self._type = type_

    # Getter for statement
    def get_statement(self) -> str:
        return self._statement

    # Setter for statement
    def set_statement(self, statement: str):
        self._statement = statement

    # Getter for related_events_indices
    def get_related_events_indices(self) -> list:
        return self._related_events_indices

    # Setter for related_events_indices
    def set_related_events_indices(self, related_events_indices: list):
        self._related_events_indices = related_events_indices

    def add_related_events_indices_by_overlap(self, all_events: list[TestEvent], overlap_events_str: list[str]):
        """
        The related events will be the value overlapped event.
        :param all_events:
        :param overlap_events_str:
        :return:
        """
        if overlap_events_str:
            index = 0
            overlap_events_set = set(overlap_events_str)
            for event in all_events:
                if event.get_statement() in overlap_events_set:
                    self._related_events_indices.append(index)
                index = index + 1

    # Add index for related_events_indices
    def add_related_events_indices(self, index: int):
        self._related_events_indices.append(index)

    # Getter for test_method_name
    def get_test_method_name(self) -> str:
        return self._test_method_name

    # Setter for test_method_name
    def set_test_method_name(self, test_method_name: str):
        self._test_method_name = test_method_name

    # Getter for is_value_overlapped
    def is_value_overlapped(self) -> bool:
        return self._is_value_overlapped

    # Setter for is_value_overlapped
    def set_is_value_overlapped(self, is_value_overlapped: bool):
        self._is_value_overlapped = is_value_overlapped

    def __str__(self):
        """
        Returns a string representation of the TestAssertion object.
        """
        return (f"TestAssertion(index={self._index}, type={self._type}, "
                f"statement='{self._statement}', related_events_indices={self._related_events_indices}, "
                f"test_method_name='{self._test_method_name}', is_value_overlapped={self._is_value_overlapped})")