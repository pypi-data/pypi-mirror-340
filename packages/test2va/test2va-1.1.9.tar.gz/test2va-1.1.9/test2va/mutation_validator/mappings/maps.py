from ..structs.EspressoCorrelations import EspressoCorrelations
from ..structs.UiAutomator1Actions import UiAutomator1Actions
from ..structs.UiAutomator1Criteria import UiAutomator1Criteria
from ..structs.UiAutomator2Actions import UiAutomator2Actions
from ..structs.UiAutomator2Criteria import UiAutomator2Criteria
from ..structs.EspressoActions import EspressoActions
from ..structs.EspressoCriteria import EspressoCriteria

# Mapping of automation frameworks to their respective action handlers
ActionMap = {
    "UiAutomator1": UiAutomator1Actions,
    "UiAutomator2": UiAutomator2Actions,
    "Espresso": EspressoActions
}
"""dict: Maps automation frameworks to their corresponding action classes."""

# Mapping of assertion correlations for specific frameworks
AssertionCorrelationMap = {
    "Espresso": EspressoCorrelations
}
"""dict: Maps automation frameworks to their respective assertion correlation handlers."""

# List of actions related to text input manipulation
TextActionMap = ["replaceText", "setText", "typeText"]
"""list: Contains names of text-related actions used in automation frameworks."""

# Mapping of automation frameworks to their corresponding criteria handlers
WebElementMap = {
    "UiAutomator1": UiAutomator1Criteria,
    "UiAutomator2": UiAutomator2Criteria,
    "Espresso": EspressoCriteria
}
"""dict: Maps automation frameworks to their respective criteria classes."""
