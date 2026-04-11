from dishka.integrations.faststream import FromDishka, inject
from faststream.kafka import KafkaRouter

from application.interactors import ProcessVideoInteractor
from config import settings
from controllers.schemas import VideoMessageStart
from infrastructure.metrics import track_message

router = KafkaRouter()


@router.subscriber(settings.kafka.topic_video_convert_start, max_workers=settings.converter.workers)
@inject
async def handle_video_convert(
    body: VideoMessageStart,
    interactor: FromDishka[ProcessVideoInteractor],
) -> None:
    async with track_message():
        await interactor.execute(video_id=body.id, video_url=body.video_url)
