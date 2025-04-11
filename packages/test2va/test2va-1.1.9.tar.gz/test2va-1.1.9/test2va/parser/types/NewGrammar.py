from typing import List, TypedDict, TypeVar, Optional, Literal, Union

"""
FullViewInteraction:
    : ViewInteraction <name> = onView(MatcherTypes<ViewMatchers>); PerformLater

ShortenedViewInteraction
    : onView(MatcherTypes<ViewMatchers>).perform(MatcherTypes<ViewMatchers>);

ReassignedViewInteraction
    : <name> = onView(MatcherTypes<ViewMatchers>);

PerformLater
    : <name>.perform(List<ViewActions>);

MatcherTypes<T>                     // Not Comprehensive
    : [Matchers.]allOf(List<T>) May be prefixed with "Matchers."
    | [Matchers.]anyOf(List<T>)
    | None (Implicitly [Matchers.]allOf(List<T>))
"""

T = TypeVar('T')
allOfType = List[T]
anyOfType = List[T]
matcherTypeList = Literal['allOf', 'anyOf']


class MatcherTypes(TypedDict):
    allOf: allOfType
    anyOf: anyOfType


"""
CharSequenceMatchers                // Not Comprehensive
    : [Matchers.]anything()         May be prefixed with "Matchers."
    | [Matchers.]is(int)
    | [Matchers.]notNullValue()
    | [Matchers.]nullValue()
    
"""

anythingType = None
izType = tuple[int]
notNullValueType = None
nullValueType = None


class CharSequenceMatchers(TypedDict):
    anything: anythingType
    iz: tuple[int]
    notNullValue: notNullValueType
    nullValue: nullValueType


"""
IntegerMatchers                     // Not Comprehensive
    : [Matchers.]anything()         May be prefixed with "Matchers."
    | [Matchers.]greaterThan(int)
    | [Matchers.]greaterThanOrEqualTo(int)
    | [Matchers.]lessThan(int)
    | [Matchers.]lessThanOrEqualTo(int)
    | [Matchers.]is(int)
    | [Matchers.]notNullValue()
    | [Matchers.]nullValue()
"""

greaterThanType = tuple[int]
greaterThanOrEqualToType = tuple[int]
lessThanType = tuple[int]
lessThanOrEqualToType = tuple[int]


class IntegerMatchers(TypedDict):
    anything: anythingType
    greaterThan: greaterThanType
    greaterThanOrEqualTo: greaterThanOrEqualToType
    lessThan: lessThanType
    lessThanOrEqualTo: lessThanOrEqualToType
    iz: izType
    notNullValue: notNullValueType
    nullValue: nullValueType


"""
ObjectMatchers                      // Not Comprehensive
    : [Matchers.]anything()         May be prefixed with "Matchers."
    | [Matchers.]is(T)
    | [Matchers.]notNullValue()
    | [Matchers.]nullValue()
"""

objectIzType = T


class ObjectMatchers(TypedDict):
    anything: anythingType
    iz: objectIzType
    notNullValue: notNullValueType
    nullValue: nullValueType


"""
StringMatchers                      // Not Comprehensive
    : [Matchers.]anything()         May be prefixed with "Matchers."
    | [Matchers.]blankOrNullString()
    | [Matchers.]blankString()
    | [Matchers.]containsString(string)
    | [Matchers.]containsStringIgnoringCase(string)
    | [Matchers.]emptyOrNullString()
    | [Matchers.]emptyString()
    | [Matchers.]endsWith(string)
    | [Matchers.]endsWithIgnoringCase(string)
    | [Matchers.]equalToCompressingWhitespace(string)
    | [Matchers.]equalToIgnoringCase(string)
    | [Matchers.]equalToIgnoringWhiteSpace(string)
    | [Matchers.]is(string)
    | [Matchers.]matchesPattern(Pattern)                    // Do not support.
    | [Matchers.]matchesPattern(string)
    | [Matchers.]matchesRegex(Pattern)                      // Do not support.
    | [Matchers.]matchesRegex(string)
    | [Matchers.]notNullValue()
    | [Matchers.]nullValue()
    | [Matchers.]startsWith(string)
    | [Matchers.]startsWithIgnoringCase(string)
    | [Matchers.]stringContainsInOrder(Iterable<String>)    // Do not support.
    | [Matchers.]stringContainsInOrder(List<String>)
"""

blankOrNullStringType = None
blankStringType = None
containsStringType = tuple[str]
containsStringIgnoringCaseType = tuple[str]
emptyOrNullStringType = None
emptyStringType = None
endsWithType = tuple[str]
endsWithIgnoringCaseType = tuple[str]
equalToCompressingWhitespaceType = tuple[str]
equalToIgnoringCaseType = tuple[str]
equalToIgnoringWhiteSpaceType = tuple[str]
stringMatcherIsType = tuple[str]
matchesPatternType = tuple[str]
matchesRegexType = tuple[str]
startsWithType = tuple[str]
startsWithIgnoringCaseType = tuple[str]
stringContainsInOrderType = List[str]


class StringMatchers(TypedDict):
    anything: anythingType
    blankOrNullString: blankOrNullStringType
    blankString: blankStringType
    containsString: containsStringType
    containsStringIgnoringCase: containsStringIgnoringCaseType
    emptyOrNullString: emptyOrNullStringType
    emptyString: emptyStringType
    endsWith: endsWithType
    endsWithIgnoringCase: endsWithIgnoringCaseType
    equalToCompressingWhitespace: equalToCompressingWhitespaceType
    equalToIgnoringCase: equalToIgnoringCaseType
    equalToIgnoringWhiteSpace: equalToIgnoringWhiteSpaceType
    iz: stringMatcherIsType
    matchesPattern: matchesPatternType
    matchesRegex: matchesRegexType
    notNullValue: notNullValueType
    nullValue: nullValueType
    startsWith: startsWithType
    startsWithIgnoringCase: startsWithIgnoringCaseType
    stringContainsInOrder: stringContainsInOrderType


"""
ViewActions
    : actionOnItemAtPosition(int, ViewActions)
    | clearText()
    | click()
    | click(ViewActions)
    | click(int, int)
    | closeSoftKeyboard()
    | doubleClick()
    | longClick()
    | openLink(MatcherTypes<StringMatchers>, ?)             // Do not support.
    | openLinkWithText(string)
    | openLinkWithText(MatcherTypes<StringMatchers>)
    | openLinkWithUri(string)
    | openLinkWithUri(UriMatcher)                           // Do not support.
    | pressBack()
    | pressBackUnconditionally()
    | pressImeActionButton()
    | pressKey(EspressoKey)                                 // Do not support.
    | pressKey(int)
    | pressMenuKey()
    | repeatedlyUntil(ViewActions, MatcherTypes<ViewMatchers>, int)
    | replaceText(string)
    | scrollTo()
    | slowSwipeLeft()
    | swipeDown()
    | swipeLeft()
    | swipeRight()
    | swipeUp()
    | typeText(string)
    | typeTextIntoFocusedView(string)
"""

actionOnItemAtPositionType = 'tuple[int, ViewActions]'
clearTextType = None
clickType = 'tuple[int | ViewActions | None, int | None]'
closeSoftKeyboardType = None
doubleClickType = None
longClickType = None
openLinkWithTextType = tuple[str | MatcherTypes[StringMatchers]]
openLinkWithUriType = tuple[str]
pressBackType = None
pressBackUnconditionallyType = None
pressImeActionButtonType = None
pressKeyType = tuple[int]
pressMenuKeyType = None
repeatedlyUntilType = 'tuple[ViewActions, MatcherTypes[ViewMatchers], int]'
replaceTextType = tuple[str]
scrollToType = None
slowSwipeLeftType = None
swipeDownType = None
swipeLeftType = None
swipeRightType = None
swipeUpType = None
typeTextType = tuple[str]
typeTextIntoFocusedViewType = tuple[str]


class ViewActions(TypedDict):
    actionOnItemAtPosition: actionOnItemAtPositionType
    clearText: clearTextType
    click: clickType
    closeSoftKeyboard: closeSoftKeyboardType
    doubleClick: doubleClickType
    longClick: longClickType
    openLinkWithText: openLinkWithTextType
    openLinkWithUri: openLinkWithUriType
    pressBack: pressBackType
    pressBackUnconditionally: pressBackUnconditionallyType
    pressImeActionButton: pressImeActionButtonType
    pressKey: pressKeyType
    pressMenuKey: pressMenuKeyType
    repeatedlyUntil: repeatedlyUntilType
    replaceText: replaceTextType
    scrollTo: scrollToType
    slowSwipeLeft: slowSwipeLeftType
    swipeDown: swipeDownType
    swipeLeft: swipeLeftType
    swipeRight: swipeRightType
    swipeUp: swipeUpType
    typeText: typeTextType
    typeTextIntoFocusedView: typeTextIntoFocusedViewType


"""
ViewMatchers
    : childAtPosition(MatcherTypes<ViewMatchers>, int)
    | doesNotHaveFocus()
    | hasBackground(int)
    | hasChildCount(int)
    | hasContentDescription()
    | hasDescendant(MatcherTypes<ViewMatchers>)
    | hasErrorText(string)
    | hasErrorText(MatcherTypes<StringMatchers>)
    | hasFocus()
    | hasImeAction(int)
    | hasImeAction(MatcherTypes<IntegerMatchers>)
    | hasLinks()
    | hasMinimumChildCount(int)
    | hasSibling(MatcherTypes<ViewMatchers>)
    | hasTextColor(int)
    | isAssignableFrom(Class<? extends View>) // Will most likely take the form <Something>. ... .clazz
    | isChecked()
    | isClickable()
    | isCompletelyDisplayed()
    | isDescendantOfA(MatcherTypes<ViewMatchers>)
    | isDisplayed()
    | isDisplayingAtLeast(int)
    | isEnabled()
    | isFocusable()
    | isFocused()
    | isJavascriptEnabled()
    | isNotChecked()
    | isNotClickable()
    | isNotEnabled()
    | isNotFocusable()
    | isNotFocused()
    | isNotSelected()
    | isRoot()
    | isSelected()
    | supportsInputMethods()
    | withAlpha(float)
    | withChild(MatcherTypes<ViewMatchers>)
    | withClassName(MatcherTypes<StringMatchers>)
    | withContentDescription(MatcherTypes<CharSequenceMatchers>)
    | withContentDescription(int)
    | withContentDescription(string)
    | withEffectiveVisibility(ViewMatchersVisibility)
    | withHint(int)
    | withHint(string)
    | withHint(MatcherTypes<StringMatchers>)
    | withId(int)
    | withId(string) // May also take the form R.id.<Something> then the result should be "Something"
    | withId(MatcherTypes<IntegerMatchers>)
    | withInputType(int)
    | withParent(MatcherTypes<ViewMatchers>)
    | withParentIndex(int)
    | withResourceName(string)
    | withResourceName(MatcherTypes<StringMatchers>)
    | withSpinnerText(int)
    | withSpinnerText(string)
    | withSpinnerText(MatcherTypes<StringMatchers>)
    | withSubstring(string)
    | withTagKey(int)
    | withTagKey(int, MatcherTypes<ObjectMatchers>)
    | withTagValue(MatcherTypes<ObjectMatchers>)
    | withText(int)
    | withText(string)
    | withText(MatcherTypes<StringMatchers>)
"""

childAtPositionType = 'tuple[MatcherTypes[ViewMatchers], int]'
doesNotHaveFocusType = None
hasBackgroundType = tuple[int]
hasChildCountType = tuple[int]
hasContentDescriptionType = None
hasDescendantType = 'tuple[MatcherTypes[ViewMatchers]]'
hasErrorTextType = tuple[str | MatcherTypes[StringMatchers]]
hasFocusType = None
hasImeActionType = tuple[int | MatcherTypes[IntegerMatchers]]
hasLinksType = None
hasMinimumChildCountType = tuple[int]
hasSiblingType = 'tuple[MatcherTypes[ViewMatchers]]'
hasTextColorType = tuple[int]
isAssignableFromType = None
isCheckedType = None
isClickableType = None
isCompletelyDisplayedType = None
isDescendantOfAType = 'tuple[MatcherTypes[ViewMatchers]]'
isDisplayedType = None
isDisplayingAtLeastType = tuple[int]
isEnabledType = None
isFocusableType = None
isFocusedType = None
isJavascriptEnabledType = None
isNotCheckedType = None
isNotClickableType = None
isNotEnabledType = None
isNotFocusableType = None
isNotFocusedType = None
isNotSelectedType = None
isRootType = None
isSelectedType = None
supportsInputMethodsType = None
withAlphaType = tuple[float]
withChildType = 'tuple[MatcherTypes[ViewMatchers]]'
withClassNameType = tuple[MatcherTypes[StringMatchers]]
withContentDescriptionType = tuple[int | str | MatcherTypes[CharSequenceMatchers]]
withEffectiveVisibilityType = None
withHintType = tuple[int | str | MatcherTypes[StringMatchers]]
withIdType = tuple[int | str | MatcherTypes[IntegerMatchers]]
withInputTypeType = tuple[int]
withParentType = 'tuple[MatcherTypes[ViewMatchers]]'
withParentIndexType = tuple[int]
withResourceNameType = tuple[str | MatcherTypes[StringMatchers]]
withSpinnerTextType = tuple[int | str | MatcherTypes[StringMatchers]]
withSubstringType = tuple[str]
withTagKeyType = tuple[int | MatcherTypes[ObjectMatchers]]
withTagValueType = tuple[MatcherTypes[ObjectMatchers]]
withTextType = tuple[int | str | MatcherTypes[StringMatchers]]

uniqueViewMatcherArgs = None | int | float | str | MatcherTypes[T]


class ViewMatchers(TypedDict):
    childAtPosition: childAtPositionType
    doesNotHaveFocus: doesNotHaveFocusType
    hasBackground: hasBackgroundType
    hasChildCount: hasChildCountType
    hasContentDescription: hasContentDescriptionType
    hasDescendant: hasDescendantType
    hasErrorText: hasErrorTextType
    hasFocus: hasFocusType
    hasImeAction: hasImeActionType
    hasLinks: hasLinksType
    hasMinimumChildCount: hasMinimumChildCountType
    hasSibling: hasSiblingType
    hasTextColor: hasTextColorType
    isAssignableFrom: isAssignableFromType
    isChecked: isCheckedType
    isClickable: isClickableType
    isCompletelyDisplayed: isCompletelyDisplayedType
    isDescendantOfA: isDescendantOfAType
    isDisplayed: isDisplayedType
    isDisplayingAtLeast: isDisplayingAtLeastType
    isEnabled: isEnabledType
    isFocusable: isFocusableType
    isFocused: isFocusedType
    isJavascriptEnabled: isJavascriptEnabledType
    isNotChecked: isNotCheckedType
    isNotClickable: isNotClickableType
    isNotEnabled: isNotEnabledType
    isNotFocusable: isNotFocusableType
    isNotFocused: isNotFocusedType
    isNotSelected: isNotSelectedType
    isRoot: isRootType
    isSelected: isSelectedType
    supportsInputMethods: supportsInputMethodsType
    withAlpha: withAlphaType
    withChild: withChildType
    withClassName: withClassNameType
    withContentDescription: withContentDescriptionType
    withEffectiveVisibility: withEffectiveVisibilityType
    withHint: withHintType
    withId: withIdType
    withInputType: withInputTypeType
    withParent: withParentType
    withParentIndex: withParentIndexType
    withResourceName: withResourceNameType
    withSpinnerText: withSpinnerTextType
    withSubstring: withSubstringType
    withTagKey: withTagKeyType
    withTagValue: withTagValueType
    withText: withTextType


"""
ViewMatchersVisibility:
    : ViewMatchers.Visibility.GONE
    | ViewMatchers.Visibility.INVISIBLE
    | ViewMatchers.Visibility.VISIBLE
"""


class MatcherComponent(TypedDict):
    Name: str
    Args: Optional[List[Union[List[str], List['ParseData']]]]


class AssertionData(TypedDict):
    Action: Optional[List['ActionData']]
    Components: List[MatcherComponent]
    MatchType: str


class MatcherData(TypedDict):
    Action: Optional[List['ActionData']]
    Components: List[MatcherComponent]
    MatchType: str


class ParseData(TypedDict):
    Assertions: List[AssertionData]
    After: List[MatcherData]
    Before: List[MatcherData]
    Matchers: List[MatcherData]
    Name: str


class ActionData(TypedDict):
    Name: str
    Args: Optional[Union[List[str], List['ParseData'], List['ActionData']]]
