from typing import Optional


class NotFoundError(Exception):
    """
    Exception that is raised when no entity is found with the given parameters.

    :param message_prefix: string that will be added before the base message
    :type message_prefix: str
    :param base_message: string that will be added after the message prefix
    :type base_message: str

    :ivar message: constructed message that will be used when exception is raised
    :type message: str
    """
    def __init__(self,
                 base_message: Optional[str] = " with the provided parameters is not found.",
                 message_prefix: Optional[str] = ""):
        self.base_message = base_message
        self.message = message_prefix + self.base_message


class AlreadyExistsError(Exception):
    """
    Exception that is raised when the entity with the given parameters already exists.

    :param message_prefix: string that will be added before the base message
    :type message_prefix: str
    """
    def __init__(self, message_prefix: Optional[str] = ""):
        self.base_message = " with the provided params already exists."
        self.message = message_prefix + self.base_message


class UnexpectedError(Exception):
    """
    Exception that is raised when server error occurs.

    :param message_postfix: string that will be added after the base message
    :type message_postfix: str

    :ivar message: constructed message that will be used when exception is raised
    :type message: str
    """
    def __init__(self, message_postfix: Optional[str] = ""):
        self.base_message = "Unexpected server error: "
        self.message = self.base_message + message_postfix


class DBError(Exception):
    """
    Exception that is raised for general database errors.

    :param message: Description of the database error
    :type message: str

    :ivar message: The error message associated with the exception
    :type message: str
    """
    def __init__(self, message):
        self.message = message
