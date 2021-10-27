from enum import Enum

class ExceptionWithCode(Exception):
    """Creates an exception that receives a Error Code and Exception message with placeholders

    >>> from enum import Enum, unique, auto
    >>> @unique
    ... class ErrorCodes(Enum):
    ...    CODE_1 = auto()
    ...
    >>> e = ExceptionWithCode(ErrorCodes.CODE_1, "Message with a {}", "placeholder")
    >>> print(e)
    [CODE_1] Message with a placeholder
    """

    def __init__(self, error_code: Enum, message: str = "", *args, **kwargs):

        # Raise a separate exception in case the error code passed isn't specified in the ErrorCodes enum
        if not isinstance(error_code, Enum):
            msg = "error_code param must be an Enum"
            raise ValueError(msg)

        self.error_code = error_code

        # Prefixing the error code to the exception message
        try:
            msg = "[{0}] {1}".format(error_code.name, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = "[{0}] {1}".format(error_code.name, message)

        super().__init__(msg)
