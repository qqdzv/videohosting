from application.exceptions.base import ApplicationExceptionError


class NotFoundError(ApplicationExceptionError):
    status_code = 404

    def __init__(self, message: str = "Not found"):
        super().__init__(message)


class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: int | None = None):
        msg = f"User with id={user_id} not found" if user_id else "User not found"
        super().__init__(msg)


class VideoNotFoundError(NotFoundError):
    def __init__(self, video_id: int):
        super().__init__(f"Video with id={video_id} not found")


class CommentNotFoundError(NotFoundError):
    def __init__(self, comment_id: int):
        super().__init__(f"Comment with id={comment_id} not found")
