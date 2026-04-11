from dishka import FromDishka
from faststream.kafka import KafkaRouter
from pydantic import BaseModel

from application.interactors.media import MarkVideoConvertFailedInteractor, SaveVideoConvertInteractor
from config import settings

router = KafkaRouter()


class VideoMessageFinish(BaseModel):
    id: int
    preview_url: str
    duration: float
    quality: str
    video_hls: str
    processing_duration: float


class VideoMessageFailed(BaseModel):
    id: int


@router.subscriber(settings.kafka.topic_video_convert_end)
async def video_convert_end_handler(
    body: VideoMessageFinish,
    interactor: FromDishka[SaveVideoConvertInteractor],
) -> None:
    await interactor.execute(
        video_id=body.id,
        preview_url=body.preview_url,
        duration=body.duration,
        quality=body.quality,
        video_hls=body.video_hls,
    )


@router.subscriber(settings.kafka.topic_video_convert_failed)
async def video_convert_failed_handler(
    body: VideoMessageFailed,
    interactor: FromDishka[MarkVideoConvertFailedInteractor],
) -> None:
    await interactor.execute(video_id=body.id)
