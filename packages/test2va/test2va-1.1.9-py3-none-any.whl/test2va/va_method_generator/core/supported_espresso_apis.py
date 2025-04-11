# supported_espresso_apis.py

# Example lists of supported matchers and actions from espresso APIs
SUPPORTED_MATCHERS = {
    "onView",
    "allOf",
    "withId",
    "withText",
    "withContentDescription",
    "withClassName",
    "withParent",
    "withParentIndex",
    "hasDescendant",

    # will be ignored by converter
    "isDisplayed",
    "containsString",
    "containsStringIgnoringCase"
}

SUPPORTED_ACTIONS = {
    "click",
    "swipeLeft",
    "swipeRight",
    "replaceText",
    "typeText",
    "longClick",
    "scrollTo"
}

# Define the set of supported non-Espresso method names
SUPPORTED_NON_ESPRESSO = {
    "closeSoftKeyboard()",
    "closeSoftKeyboard();",
    "pressBack()",
    "pressBack();"
}
