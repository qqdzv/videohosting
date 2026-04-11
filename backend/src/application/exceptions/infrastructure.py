from application.exceptions.base import ApplicationExceptionError


class InfrastructureError(ApplicationExceptionError):
    status_code = 500


class StorageError(InfrastructureError):
    def __init__(self, message: str):
        super().__init__(f"Storage error: {message}")


class MessageBrokerError(InfrastructureError):
    def __init__(self, message: str):
        super().__init__(f"Message broker error: {message}")


class CacheError(InfrastructureError):
    def __init__(self, message: str):
        super().__init__(f"Cache error: {message}")
