from application.exceptions.base import ApplicationExceptionError


class ValidationError(ApplicationExceptionError):
    status_code = 422


class SelfSubscriptionError(ValidationError):
    def __init__(self):
        super().__init__("Cannot subscribe to yourself")
