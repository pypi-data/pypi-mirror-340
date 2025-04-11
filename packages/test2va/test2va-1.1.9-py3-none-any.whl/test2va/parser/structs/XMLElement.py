import xml.etree.ElementTree as Et

from collections import deque
from typing import Callable, List, Optional


class XMLElement(Et.Element):
    """
    A wrapper class for `xml.etree.ElementTree.Element` that provides additional functionality for XML element traversal,
    parent-child relationships, indexing, and transformations.

    Attributes:
        INDEX_COUNTER (int): A counter for assigning unique indices to elements.
    """
    INDEX_COUNTER = 1

    def __init__(self, tag: str, attrib: dict = {}, **extra):
        """
        Initializes an XMLElement.

        Args:
            tag (str): The tag of the XML element.
            attrib (dict, optional): A dictionary of attributes for the element. Defaults to an empty dictionary.
            **extra: Additional keyword arguments passed to the superclass.
        """
        super().__init__(tag, attrib, **extra)
        self._parent: Optional["XMLElement"] = None
        self._depth: int = 0
        self._index: int = 0
        self._df_index: int = 0
        self._text: Optional[str] = None

    def get_parent(self) -> Optional["XMLElement"]:
        """
        Returns the parent of the current XML element.

        Returns:
            Optional[XMLElement]: The parent element if it exists, otherwise None.
        """
        return self._parent

    def get_siblings(self) -> List["XMLElement"]:
        """
        Returns a list of sibling elements (excluding itself).

        Returns:
            List[XMLElement]: A list of sibling elements.
        """
        if self._parent is not None:
            return [elem for elem in self._parent.get_children() if elem != self]
        return []

    def get_children(self) -> List["XMLElement"]:
        """
        Returns a list of child elements.

        Returns:
            List[XMLElement]: A list of child elements.
        """
        return list(self)

    def append(self, element: "XMLElement"):
        """
        Appends a child element and updates its metadata.

        Args:
            element (XMLElement): The child element to append.
        """
        super().append(element)
        element._parent = self
        element._depth = self._depth + 1
        element.set_index(XMLElement.INDEX_COUNTER)
        element._df_index = 0
        XMLElement.INDEX_COUNTER += 1

    def remove(self, element: "XMLElement"):
        """
        Removes a child element and updates its metadata.

        Args:
            element (XMLElement): The child element to remove.
        """
        super().remove(element)
        element._parent = None
        element._depth = 0

    def depth(self) -> int:
        """
        Returns the depth level of the current element in the tree.

        Returns:
            int: The depth level.
        """
        return self._depth

    def find_first_child(self, callback: Callable[["XMLElement"], bool]) -> Optional["XMLElement"]:
        """
        Finds the first child element that matches a given condition.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each child.

        Returns:
            Optional[XMLElement]: The first matching child element, or None if no match is found.
        """
        for child in self:
            if callback(child):
                return child
        return None

    def find_first_descendant(self, callback: Callable[["XMLElement"], bool]) -> Optional["XMLElement"]:
        """
        Finds the first descendant element that matches a given condition using BFS.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each descendant.

        Returns:
            Optional[XMLElement]: The first matching descendant element, or None if no match is found.
        """
        for child in self:
            if callback(child):
                return child
            descendant_result = child.find_first_descendant(callback)
            if descendant_result is not None:
                return descendant_result
        return None

    def find_children(self, callback: Callable[["XMLElement"], bool]) -> List["XMLElement"]:
        """
        Finds all child elements that match a given condition.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each child.

        Returns:
            List[XMLElement]: A list of matching child elements.
        """
        return [child for child in list(self) if callback(child)]

    def find_descendants(self, callback: Callable[["XMLElement"], bool]) -> List["XMLElement"]:
        """
        Finds all descendant elements that match a given condition using BFS.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each descendant.

        Returns:
            List[XMLElement]: A list of matching descendant elements.
        """
        descendants: List[XMLElement] = []
        queue = deque([self])

        while queue:
            element = queue.popleft()

            if callback(element):
                descendants.append(element)

            queue.extend(element.get_children())

        return descendants

    def find_descendants_dfs(self, callback: Callable[["XMLElement"], bool]) -> List["XMLElement"]:
        """
        Finds all descendant elements that match a given condition using DFS.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each descendant.

        Returns:
            List[XMLElement]: A list of matching descendant elements.
        """
        descendants: List[XMLElement] = []
        stack = [self]  # Use a stack for DFS

        while stack:
            element = stack.pop()  # Get the last element added (DFS behavior)

            if callback(element):
                descendants.append(element)

            # Add children to the stack in reverse order so that they are processed in the original order
            stack.extend(reversed(element.get_children()))

        return descendants

    def find_first_parent(self, callback: Callable[["XMLElement"], bool]) -> Optional["XMLElement"]:
        """
        Finds the first parent element that matches a given condition.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each parent.

        Returns:
            Optional[XMLElement]: The first matching parent element, or None if no match is found.
        """
        parent = self.get_parent()
        while parent is not None:
            if callback(parent):
                return parent
            parent = parent.get_parent()
        return None

    def find_first_ancestor(self, callback: Callable[["XMLElement"], bool]) -> Optional["XMLElement"]:
        """
        Finds the first ancestor element that matches a given condition.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each ancestor.

        Returns:
            Optional[XMLElement]: The first matching ancestor element, or None if no match is found.
        """
        ancestor = self.find_first_parent(callback)
        if ancestor is None:
            ancestor = self.find_parents(callback)
        return ancestor

    def find_parents(self, callback: Callable[["XMLElement"], bool]) -> List["XMLElement"]:
        """
        Finds all parent elements that match a given condition.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each parent.

        Returns:
            List[XMLElement]: A list of matching parent elements.
        """
        parents: List[XMLElement] = []
        parent = self.get_parent()
        while parent is not None:
            if callback(parent):
                parents.append(parent)
            parent = parent.get_parent()
        return parents

    def find_ancestors(self, callback: Callable[["XMLElement"], bool]) -> List["XMLElement"]:
        """
        Finds all ancestor elements that match a given condition.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each ancestor.

        Returns:
            List[XMLElement]: A list of matching ancestor elements.
        """
        ancestors: List[XMLElement] = []
        parent = self.get_parent()
        while parent is not None:
            if callback(parent):
                ancestors.append(parent)
            parent = parent.get_parent()
        return ancestors

    def is_a_descendant_of(self, callback: Callable[["XMLElement"], bool]) -> bool:
        """
        Checks if the current element is a descendant of an element that matches a given condition.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each ancestor.

        Returns:
            bool: True if the element is a descendant of a matching element, otherwise False.
        """
        parent = self.get_parent()
        while parent is not None:
            if callback(parent):
                return True
            parent = parent.get_parent()
        return False

    def is_a_child_of(self, callback: Callable[["XMLElement"], bool]) -> bool:
        """
        Checks if the current element is a child of an element that matches a given condition.

        Args:
            callback (Callable[[XMLElement], bool]): A function that evaluates each parent.

        Returns:
            bool: True if the element is a child of a matching element, otherwise False.
        """
        parent = self.get_parent()
        if parent is not None and callback(parent):
            return True
        return False

    def set_index(self, index: int):
        """
        Sets the index of the current element.

        Args:
            index (int): The index to set.
        """
        self._index = index

    def index(self, **kwargs) -> int:
        """
        Returns the index of the current element.

        Returns:
            int: The index value.
        """
        return self._index

    def as_uis1(self) -> "UiSelector1ExprElement":
        from test2va.parser.structs.UiAutomator1ExprElement import UiAutomator1ExprElement as UIA1E
        u_expr = UIA1E(self.tag, self.attrib)
        u_expr.tag = self.tag
        u_expr.attrib = self.attrib
        u_expr._text = self._text
        u_expr._parent = self._parent
        u_expr._depth = self._depth
        u_expr._index = self._index
        u_expr._element = self
        return u_expr

    def as_uia2(self) -> "UiAutomator2ExprElement":
        from test2va.parser.structs.UiAutomator2ExprElement import UiAutomator2ExprElement as UIA2E
        u2_expr = UIA2E(self)
        u2_expr.tag = self.tag
        u2_expr.attrib = self.attrib
        u2_expr.text = self.text
        u2_expr._parent = self._parent
        u2_expr._depth = self._depth
        u2_expr._index = self._index
        u2_expr._element = self
        return u2_expr

    def as_espresso_decl(self) -> "EspressoDeclElement":
        """
        Converts the current element into a `EspressoDeclElement`.

        Returns:
            EspressoDeclElement: A new instance of `EspressoDeclElement` representing the current element.
        """
        from test2va.parser.structs.EspressoDeclElement import EspressoDeclElement as EDE
        e_decl = EDE(self)
        e_decl.tag = self.tag
        e_decl.attrib = self.attrib
        e_decl.text = self.text
        e_decl._parent = self._parent
        e_decl._depth = self._depth
        e_decl._index = self._index
        e_decl._element = self
        return e_decl

    @property
    def text(self):
        """
        Returns the text content of the element.

        Returns:
            str: The text content of the element.
        """
        return self._text or ""

    @text.setter
    def text(self, value: str):
        """
        Sets the text content of the element.

        Args:
            value (str): The text value to set.
        """
        self._text = value

    def _extend_element(self, element: "XMLElement"):
        """
        Extends the current element with attributes from another element.

        Args:
            element (XMLElement): The element to extend from.
        """
        # Copy attributes from the original element
        self.tag = element.tag
        self.attrib = element.attrib

        # Copy the text content
        self._text = element.text

    def get_df_index(self) -> int:
        """
        Returns the depth-first index of the element.

        Returns:
            int: The depth-first index.
        """
        return self._df_index

    def set_df_index(self, index: int):
        """
        Sets the depth-first index of the element.

        Args:
            index (int): The index to set.
        """
        self._df_index = index

    def __getattr__(self, attr: str):
        # Forward attribute access to the underlying Element object
        return getattr(super(), attr)

    def __repr__(self):
        """
        Returns a string representation of the XMLElement.

        Returns:
            str: A string representation of the XMLElement.
        """
        return f"XMLElement(tag='{self.tag}')"
