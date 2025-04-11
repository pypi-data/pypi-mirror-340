class MasterError(Exception):
    """Base exception class for handling errors in the Test2VA framework.

    This exception fires error and finish events when an error occurs.

    Args:
        message (str): The error message.
        events: Event handler object that fires `on_error` and `on_finish` events.
    """

    def __init__(self, message: str, events):
        self.message = message
        events.on_error.fire(message, self)
        events.on_finish.fire()


class NoJavaData(MasterError):
    """Exception raised when Java data is missing."""
    pass


class CapTypeMismatch(MasterError):
    """Exception raised when there is a mismatch in capability type."""
    pass


class ApiKeyError(MasterError):
    """Exception raised for API key-related issues."""
    pass


class NodeNotInstalled(MasterError):
    """Exception raised when Node.js is not installed."""
    pass


class ExecutionStopped(MasterError):
    """Exception raised when the execution is manually or forcefully stopped."""
    pass


class AppiumInstallationError(MasterError):
    """Exception raised when there is an issue with Appium installation."""
    pass


class AppiumServerError(MasterError):
    """Exception raised when the Appium server encounters an error."""
    pass


class SRCMLError(MasterError):
    """Exception raised when there is an issue with SRCML (Source Code Markup Language) parsing."""
    pass


class JSONError(MasterError):
    """Exception raised when there is an issue with JSON parsing or formatting."""
    pass


class ParseError(MasterError):
    """Exception raised when there is an error parsing Java source code."""
    pass


class MutatorError(MasterError):
    """Exception raised when an error occurs in the mutation process."""
    pass


class GeneratorError(MasterError):
    """Exception raised when an error occurs during test case generation."""
    pass
