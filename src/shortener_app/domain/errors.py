from typing import Optional


class NotFoundError(Exception):
    def __init__(
            self,
            base_message: Optional[str] = " with the provided parameters is not found.",
            message_prefix: Optional[str] = ""
    ):
        self.base_message = base_message
        self.message = message_prefix + self.base_message


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


class AccessDeniedError(Exception):
    def __init__(self, message: Optional[str] = "Invalid credentials."):
        self.message = message


class CurrentUserError(Exception):
    def __init__(self, message: Optional[str] = "Unavailable operation."):
        self.message = message


class AlreadyExistsError(Exception):
    def __init__(self, message_prefix: Optional[str] = ""):
        self.base_message = " with the provided params already existsts."
        self.message = message_prefix + self.base_message


class UnexpectedError(Exception):
    def __init__(self, message_postfix: Optional[str] = ""):
        self.base_message = "Unexpected server error: "
        self.message = self.base_message + message_postfix


class DBError(Exception):
    def __init__(self, message):
        self.message = message