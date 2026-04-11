from pydantic import BaseModel


class VideoMessageStart(BaseModel):
    id: int
    video_url: str
