from application.exceptions.base import ApplicationExceptionError


class AuthenticationError(ApplicationExceptionError):
    status_code = 401

    def __init__(self, message: str = "Invalid Bearer Token"):
        super().__init__(message)


class InvalidCredentialsError(ApplicationExceptionError):
    status_code = 401

    def __init__(self):
        super().__init__("Invalid email or password")


class UserAlreadyExistsError(ApplicationExceptionError):
    status_code = 409

    def __init__(self, field: str, value: str):
        super().__init__(f"User with {field}='{value}' already exists")
