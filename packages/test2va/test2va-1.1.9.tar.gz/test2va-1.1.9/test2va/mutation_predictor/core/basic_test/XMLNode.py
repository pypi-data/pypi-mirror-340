from test2va.mutation_predictor.core.basic_test.TestTypes import ElementMatchingType


class XMLNode:
    def __init__(self, node_value: str, matching_type: ElementMatchingType, node_with_context: str = None):
        """
        Initializes the XMLNode class.

        Args:
            node_value (str): The value of the node.
            matching_type (ElementMatchingType): The type of the sibling.
            node_with_context (str, optional): Additional context for the node. Defaults to None.
        """
        self._node_value = node_value
        self._node_type = matching_type
        self._node_with_context = node_with_context

    # Getter for node_value
    def get_node_value(self) -> str:
        return self._node_value

    # Setter for node_value
    def set_node_value(self, node_value: str):
        self._node_value = node_value

    # Getter for sibling_type
    def get_matching_type(self) -> ElementMatchingType:
        return self._node_type

    # Setter for sibling_type
    def set_matching_type(self, sibling_type: ElementMatchingType):
        self._node_type = sibling_type

    # Getter for node_with_context
    def get_node_with_context(self) -> str:
        return self._node_with_context

    # Setter for node_with_context
    def set_node_with_context(self, node_with_context: str):
        self._node_with_context = node_with_context

    # String representation of the XMLNode object
    def __str__(self):
        return (f"XMLNode(node_value='{self._node_value}', "
                f"sibling_type={self._node_type.name}, "
                f"node_with_context='{self._node_with_context}')")