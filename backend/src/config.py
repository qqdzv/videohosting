import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEDIR = Path(__file__).resolve().parent.parent


class PostgresConfig(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int = 0

    @property
    def url(self) -> str:
         return f"redis://{self.host}:{self.port}/{self.db}"


class KafkaConfig(BaseModel):
    server: str
    topic_user_created: str = "user.created"
    topic_user_logged_in: str = "user.logged_in"
    topic_user_logged_out: str = "user.logged_out"
    topic_comment_created: str = "comment.created"
    topic_subscription_created: str = "subscription.created"
    topic_video_convert_start: str = "video.convert.start"
    topic_video_convert_end: str = "video.convert.end"
    topic_video_convert_failed: str = "video.convert.failed"
    topic_video_published: str = "video.published"


class S3Config(BaseModel):
    region_name: str
    endpoint_url: str
    access_key: str
    secret_key: str
    bucket: str
    public_url: str


class JWTConfig(BaseModel):
    private_key_path: str = "/run/secrets/jwt/private.pem"
    public_key_path: str = "/run/secrets/jwt/public.pem"
    algorithm: str = "RS256"
    token_ttl_seconds: int = 60 * 60 * 24 * 7  # 7 days

    @property
    def private_key(self) -> str:
        return Path(self.private_key_path).read_text()

    @property
    def public_key(self) -> str:
        return Path(self.public_key_path).read_text()


class LoggingConfig(BaseModel):
    level: int = logging.INFO
    use_json: bool = False


class Config(BaseSettings):
    debug: bool = False

    postgres: PostgresConfig
    redis: RedisConfig
    kafka: KafkaConfig
    s3: S3Config
    jwt: JWTConfig
    logging: LoggingConfig = LoggingConfig()

    model_config = SettingsConfigDict(
        extra="ignore",
        populate_by_name=True,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=str(BASEDIR / ".env"),
    )


settings = Config()  # ty: ignore[missing-argument]
