from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEDIR = Path(__file__).resolve().parent.parent


class KafkaConfig(BaseModel):
    server: str
    topic_video_convert_start: str = "video.convert.start"
    topic_video_convert_end: str = "video.convert.end"
    topic_video_convert_error: str = "video.convert.failed"


class S3Config(BaseModel):
    region_name: str
    endpoint_url: str
    access_key: str
    secret_key: str
    bucket: str
    public_url: str


class ConverterConfig(BaseModel):
    workers: int = 1


class MetricsConfig(BaseModel):
    port: int = 80


class Config(BaseSettings):
    kafka: KafkaConfig
    s3: S3Config
    converter: ConverterConfig = ConverterConfig()
    metrics: MetricsConfig = MetricsConfig()

    model_config = SettingsConfigDict(
        extra="ignore",
        populate_by_name=True,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=str(BASEDIR / ".env"),
    )


settings = Config()  # ty: ignore[missing-argument]
