# Enum for Type
from enum import Enum

class AssertionType(Enum):
    """
    An enum class representing different types of assertions.

    Attributes:
        Type1: Assert a set pre-defined value.
        Type2: Assert typed in value.
        Type3: Assert the deleted value.
        Type4: ?
    """
    Type1 = 1
    Type2 = 2
    Type3 = 3
    Type4 = 4


class EventType(Enum):
    """
    An enum class representing different types of event.
    actionOnItemAtPosition() is not supported currently

    Attributes:
        Type1: click event: click(), doubleClick(), longClick()
        Type2: input event: typeText(), replaceText(), clearText()
        Type3: scroll event: scrollTo(), scrollTo(matcher)
        Type4: swipe event: swipeleft(), swiperight()
        Type5: none of them event
    """
    Type1 = 11
    Type2 = 12
    Type3 = 13
    Type4 = 14
    Type5 = 15


class ScrollType(Enum):
    """
    An enum class representing different types of scroll event.

    Attributes:
        Type1: scrollTo() in scrollView
        Type2: scrollTo(matcher) in recycle view
    """
    Type1 = 21
    Type2 = 22


class ElementMatchingType(Enum):
    """
    An enum class representing different types of sibling nodes context

    Attributes:
        Type1: none-of-them
        Type2: has parent()
        Type3: has Descendant
        Type4: use both of them
    """
    Type1 = 31
    Type2 = 32
    Type3 = 33
    Type4 = 34