from test2va.mutation_predictor.core.basic_test.MutantEvent import MutantEvent
from test2va.mutation_predictor.core.basic_test.TestTypes import AssertionType


class TestEvent:
    def __init__(self, index: int = None, statement: str = "", related_assertion_indices: list = None,
                 test_method_name: str = "", overlap_value: str = "", event_type: AssertionType = None,
                 mutant_events: list[MutantEvent] = None, has_overlap: bool = False,
                 is_mutable: bool = False, xpath: str = ""):
        """
        Initializes the TestEvent class. Allows empty constructor.

        Args:
            index (int, optional): The index of the event. Defaults to None.
            statement (str, optional): The statement associated with the event. Defaults to an empty string.
            related_assertion_indices (list of int, optional): A list of indices that relate to assertions. Defaults to None.
            test_method_name (str, optional): The name of the test method associated with this event. Defaults to an empty string.
            overlap_value (str, optional): The value of the overlap. Defaults to an empty string.
            event_type (AssertionType, optional): The type of the event. Defaults to None.
            mutant_events (list of MutantEvent, optional): A list of MutantEvent objects. Defaults to None.
            has_overlap (bool, optional): Indicates if there is an overlap. Defaults to False.
            is_mutable (bool, optional): Indicates if the event is mutable. Defaults to False.
            xpath (str, optional): xpath of the current event
        """
        self._index = index
        self._statement = statement
        self._related_assertion_indices = related_assertion_indices if related_assertion_indices is not None else []
        self._test_method_name = test_method_name
        self._overlap_value = overlap_value
        self._event_type = event_type
        self._mutant_events = mutant_events if mutant_events is not None else []
        self._has_overlap = has_overlap
        self._is_mutable = is_mutable
        self._xpath = xpath
        self._mutant_candidates_before = 0
        self._mutant_candidates_after = 0

    # Getter for index
    def get_index(self) -> int:
        return self._index

    # Setter for index
    def set_index(self, index: int):
        self._index = index

    # Getter for statement
    def get_statement(self) -> str:
        return self._statement

    # Setter for statement
    def set_statement(self, statement: str):
        self._statement = statement

    # Getter for related_assertion_indices
    def get_related_assertion_indices(self) -> list:
        return self._related_assertion_indices

    # Setter for related_assertion_indices
    def set_related_assertion_indices(self, related_assertion_indices: list):
        self._related_assertion_indices = related_assertion_indices

    # Add index for related_assertion_indices
    def add_related_assertion_indices(self, index: int):
        self._related_assertion_indices.append(index)

    def add_related_assertion_indices_by_overlap(self, index, overlap_events_str):
        if overlap_events_str:
            overlap_events_set = set(overlap_events_str)
            if self._statement in overlap_events_set:
                self._related_assertion_indices.append(index)

    # Getter for test_method_name
    def get_test_method_name(self) -> str:
        return self._test_method_name

    # Setter for test_method_name
    def set_test_method_name(self, test_method_name: str):
        self._test_method_name = test_method_name

    # Getter for overlap_value
    def get_overlap_value(self) -> str:
        return self._overlap_value

    # Setter for overlap_value
    def set_overlap_value(self, overlap_value: str):
        if overlap_value:
            self._overlap_value = overlap_value
            self.set_has_overlap(True)

    def set_overlap_value_by_overlap_report(self, overlap_values: list[str]):
        if overlap_values:
            overlap_values_set = set(overlap_values)
            for value in overlap_values_set:
                if value in self._statement:
                    self._overlap_value = value
                    self.set_has_overlap(True)

    # Getter for event_type
    def get_event_type(self) -> AssertionType:
        return self._event_type

    # Setter for event_type
    def set_event_type(self, event_type: AssertionType):
        self._event_type = event_type

    # Getter and Setter for mutant_events
    def get_mutant_events(self) -> list[MutantEvent]:
        return self._mutant_events

    def set_mutant_events(self, mutant_events: list[MutantEvent]):
        if mutant_events:
            self._set_is_mutable(True)
            self._mutant_events = mutant_events

    def add_mutant_event(self, mutant_event: MutantEvent):
        self._mutant_events.append(mutant_event)

    # Getter and Setter for has_overlap
    def get_has_overlap(self) -> bool:
        return self._has_overlap

    def set_has_overlap(self, has_overlap: bool):
        self._has_overlap = has_overlap

    # Getter and Setter for is_mutable
    def get_is_mutable(self) -> bool:
        return self._is_mutable

    def _set_is_mutable(self, is_mutable: bool):
        self._is_mutable = is_mutable

    def get_xpath(self) -> str:
        return self._xpath

    # Setter for xpath
    def set_xpath(self, xpath: str):
        self._xpath = xpath

    def __str__(self):
        """
        Returns a string representation of the TestEvent object.
        """
        return (f"TestEvent(index={self._index}, statement='{self._statement}', "
                f"related_assertion_indices={self._related_assertion_indices}, "
                f"test_method_name='{self._test_method_name}', "
                f"overlap_value='{self._overlap_value}', event_type='{self._event_type}', "
                f"mutant_events={self._mutant_events}, has_overlap={self._has_overlap}, "
                f"is_mutable={self._is_mutable}, mutant_candidates_before={self._mutant_candidates_before}"
                f"mutant_candidates_after={self._mutant_candidates_after}")

    def set_mutant_candidates_before(self, number: int):
        self._mutant_candidates_before = number

    def set_mutant_candidates_after(self, number: int):
        self._mutant_candidates_after = number

    def get_mutant_candidates_before(self):
        return self._mutant_candidates_before

    def get_mutant_candidates_after(self):
        return self._mutant_candidates_after

