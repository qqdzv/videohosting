import asyncio
import tempfile
import time
import uuid
from dataclasses import dataclass
from functools import partial
from pathlib import Path

import ffmpeg

from application.events import VideoConvertedEndEvent, VideoConvertFailedEvent
from application.interfaces import EventPublisher, StorageService


@dataclass
class ProcessVideoInteractor:
    _storage: StorageService
    _event_publisher: EventPublisher

    async def execute(self, video_id: int, video_url: str) -> None:
        try:
            await self._process(video_id, video_url)
        except Exception:
            await self._event_publisher.publish(VideoConvertFailedEvent(id=video_id))
            raise

    async def _process(self, video_id: int, video_url: str) -> None:
        started_at = time.monotonic()
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            tempfile.NamedTemporaryFile(suffix=".mp4") as download_file,
            tempfile.NamedTemporaryFile(suffix=".m3u8") as m3u8_file,
            tempfile.NamedTemporaryFile(suffix=".jpg") as preview_file,
        ):
            await self._storage.download_file(video_url, download_file.name)

            unique_folder = str(uuid.uuid4())

            await asyncio.to_thread(
                ffmpeg
                .input(download_file.name, ss=1)
                .output(preview_file.name, vframes=1)
                .run,
                capture_stdout=True,
                capture_stderr=True,
                overwrite_output=True,
            )

            preview_url = await self._storage.upload_file(
                preview_file.name,
                f"{unique_folder}/preview.jpg",
                content_type="image/jpeg",
            )

            probe = await asyncio.to_thread(ffmpeg.probe, download_file.name)
            duration = float(probe["format"]["duration"])

            video_stream = next(
                s for s in probe["streams"] if s.get("codec_type") == "video"
            )
            width = video_stream["width"]
            height = video_stream["height"]
            quality = f"{width}x{height}"

            hls_base_url = await self._storage.get_url(f"{unique_folder}/")
            await asyncio.to_thread(
                partial(
                    ffmpeg
                    .input(download_file.name)
                    .output(
                        m3u8_file.name,
                        hls_time=6,
                        hls_list_size=0,
                        ac=2,
                        hls_segment_filename=f"{temp_dir}/%05d.ts",
                        hls_base_url=hls_base_url,
                    )
                    .run,
                    overwrite_output=True,
                ),
            )

            await self._storage.upload_file(
                m3u8_file.name,
                f"{unique_folder}/playlist.m3u8",
                content_type="application/vnd.apple.mpegurl",
            )

            for file in Path(temp_dir).iterdir():
                await self._storage.upload_file(
                    str(file),
                    f"{unique_folder}/{file.name}",
                    content_type="video/mp2t",
                )

            video_hls = await self._storage.get_url(f"{unique_folder}/playlist.m3u8")

            await self._event_publisher.publish(
                VideoConvertedEndEvent(
                    id=video_id,
                    preview_url=preview_url,
                    duration=duration,
                    quality=quality,
                    video_hls=video_hls,
                    processing_duration=round(time.monotonic() - started_at, 2),
                ),
            )
