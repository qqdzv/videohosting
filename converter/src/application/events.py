from dataclasses import dataclass


class DomainEvent:
    pass


@dataclass(frozen=True)
class VideoConvertedEndEvent(DomainEvent):
    id: int
    preview_url: str
    duration: float
    quality: str
    video_hls: str
    processing_duration: float


@dataclass(frozen=True)
class VideoConvertFailedEvent(DomainEvent):
    id: int
