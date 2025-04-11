from test2va.va_method_generator.core.mutant_report_parser import Event
from test2va.va_method_generator.core.supported_espresso_apis import SUPPORTED_MATCHERS, SUPPORTED_ACTIONS


class UnsupportedMatcherException(Exception):
    """Raised when an unsupported matcher is found."""

    def __init__(self, unsupported_matchers):
        message = f"Unsupported matcher(s): {', '.join(unsupported_matchers)}. Supported matchers: {', '.join(SUPPORTED_MATCHERS)}"
        super().__init__(message)


class UnsupportedActionException(Exception):
    """Raised when an unsupported action is found."""

    def __init__(self, unsupported_actions):
        message = f"Unsupported action(s): {', '.join(unsupported_actions)}. Supported actions: {', '.join(SUPPORTED_ACTIONS)}"
        super().__init__(message)


class UnsupportedEventException(Exception):
    """Exception raised for unsupported events."""
    def __init__(self, event: Event):
        message = (f"Unsupported event:\n"
                   f"  is_mutable: {event.is_mutable()}\n"
                   f"  parameter: {event.get_parameter()}\n"
                   f"  original_statement: {event.get_original_statement()}")
        super().__init__(message)


class UnsupportedNonEspressoStatementException(Exception):
    """Exception raised when a statement is not supported."""
    def __init__(self, statement):
        super().__init__(f"Unsupported Non-Espresso statement: {statement}")


class OldStatementMissingInReportException(Exception):
    """Exception raised when a statement is not in the mutant report."""
    def __init__(self, statement):
        super().__init__(f"Old statement is missing in the mutant report: {statement}")


class IllegalMethodFormatException(Exception):
    """Exception raised when a method is in wrong format."""
    def __init__(self, method_str):
        super().__init__(f"illegal format of the method: {method_str}")


class PreDefinedDecisionUndeterminedException(Exception):
    """Custom exception for errors related to the method generation process."""

    def __init__(self, message: str):
        super().__init__(message)