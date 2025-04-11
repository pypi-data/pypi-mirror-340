class EspressoMatchTypes:
    """Provides matching logic for Espresso-based UI element criteria."""

    @staticmethod
    def allOf(funcs):
        """Checks if all provided functions return True for a given element.

        Args:
            funcs (list): A list of functions that take an XMLElement as input and return a boolean.

        Returns:
            function: A callable function that evaluates whether all functions return True for a given element.
        """
        def f(e):
            return all(fun(e) for fun in funcs)

        return f

    @staticmethod
    def anyOf(funcs):
        """Checks if any of the provided functions return True for a given element.

        Args:
            funcs (list): A list of functions that take an XMLElement as input and return a boolean.

        Returns:
            function: A callable function that evaluates whether at least one function returns True for a given element.
        """
        def f(e):
            return any(fun(e) for fun in funcs)

        return f
