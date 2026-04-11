from application.exceptions.base import ApplicationExceptionError


class PermissionDeniedError(ApplicationExceptionError):
    status_code = 403

    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class NotYourVideoError(PermissionDeniedError):
    def __init__(self, message: str = "It's not your video"):
        super().__init__(message)


class NotYourCommentError(PermissionDeniedError):
    def __init__(self, message: str = "It's not your comment"):
        super().__init__(message)
