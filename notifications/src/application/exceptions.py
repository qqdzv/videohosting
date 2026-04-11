class ApplicationExceptionError(Exception):
    status_code: int = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(ApplicationExceptionError):
    status_code = 401

    def __init__(self, message: str = "Invalid Bearer Token"):
        super().__init__(message)


class NotificationNotFoundError(ApplicationExceptionError):
    status_code = 404

    def __init__(self):
        super().__init__("Notification not found")


class NotificationPermissionError(ApplicationExceptionError):
    status_code = 403

    def __init__(self):
        super().__init__("Permission denied")
