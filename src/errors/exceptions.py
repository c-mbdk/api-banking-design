import sys
import traceback


class BaseException(Exception):
    """
    Base class for custom exceptions.

    Retrieves information about where the error occurred for future fixes.
    """

    def __init__(self, message):
        self.message = message
        print(sys.exc_info())
        current_frame = traceback.extract_tb(sys.exc_info()[2])[-1]
        self.line_number = current_frame.lineno
        self.method_name = current_frame.name

    def __str__(self):
        return f"""
        Error: {self.message} (Line: {self.line_number}, Method: {self.method_name})
        """


class DBConfigError(BaseException):
    """Raised when db configuration fails."""

    pass
