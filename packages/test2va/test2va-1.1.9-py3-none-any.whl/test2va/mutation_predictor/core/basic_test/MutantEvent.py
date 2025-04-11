class MutantEvent:
    def __init__(self, index: int, xpath: str, statement: str):
        """
        Initializes the MutantEvent class.

        Args:
            index (int): The index of the mutant event.
            xpath (str): The XPath expression associated with the event.
            statement (str): The statement associated with the mutant event.
            assertion_statement {str: str}: The assertion statement associated with the index.
        """
        self.index = index
        self.xpath = xpath
        self.statement = statement
        self.assertion_statement_pairs: dict = {}

    # Getter for index
    def get_index(self) -> int:
        return self.index

    # Setter for index
    def set_index(self, index: int):
        self.index = index

    # Getter for xpath
    def get_xpath(self) -> str:
        return self.xpath

    # Setter for xpath
    def set_xpath(self, xpath: str):
        self.xpath = xpath

    # Getter for statement
    def get_statement(self) -> str:
        return self.statement

    # Setter for statement
    def set_statement(self, statement: str):
        self.statement = statement

    # Getter for assertion_statement
    def get_assertion_statement_pairs(self) -> dict:
        return self.assertion_statement_pairs

    # Setter for assertion_statement
    def set_assertion_statement_pairs(self, mutant_assertions_str: list[str], original_assertions_str: list[str]):
        """
        Set the assertion_statement_pairs by comparing the mutant_assertions list and the original assertions list.
        If original assertions list is:
            onView(withText(containsString("4"))).check(matches(isDisplayed()));
            onView(withText(containsString("PM"))).check(matches(isDisplayed()));
        And the mutant assertion list is:
            onView(withText(containsString("12"))).check(matches(isDisplayed()));
            onView(withText(containsString("PM"))).check(matches(isDisplayed()));

        The assertion_statement_pairs should be:
            { 0: "onView(withText(containsString("12"))).check(matches(isDisplayed()));" }
        :param mutant_assertions_str: gpt suggested updated assertions for mutant event
        :param original_assertions_str: original assertions from test method
        :return:
        """

        # make sure the two lists have the same length
        if len(mutant_assertions_str) != len(original_assertions_str):
            return

        index = 0
        for mutant_assertion in mutant_assertions_str:
            # add to pair when the mutant assertion is different from the original ones
            if mutant_assertion != original_assertions_str[index]:
                self.assertion_statement_pairs[str(index)] = mutant_assertion
            index = index + 1

    def __str__(self):
        """
        Returns a string representation of the MutantEvent object.
        """
        return (f"MutantEvent(index={self.index}, xpath='{self.xpath}', statement='{self.statement}', "
                f"assertion_statement_pairs='{self.assertion_statement_pairs}')")

