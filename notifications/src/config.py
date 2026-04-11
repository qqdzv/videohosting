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
    host: str = "redis_app"
    port: int = 6379
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
    topic_video_published: str = "video.published"


class JWTConfig(BaseModel):
    private_key_path: str = "/run/secrets/jwt/private.pem"
    public_key_path: str = "/run/secrets/jwt/public.pem"
    algorithm: str = "RS256"

    @property
    def private_key(self) -> str:
        return Path(self.private_key_path).read_text()

    @property
    def public_key(self) -> str:
        return Path(self.public_key_path).read_text()

class LoggingConfig(BaseModel):
    level: int = logging.INFO
    use_json: bool = False


class EmailConfig(BaseModel):
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str
    sender_password: str


class Config(BaseSettings):
    debug: bool

    postgres: PostgresConfig
    kafka: KafkaConfig
    redis: RedisConfig = RedisConfig()
    jwt: JWTConfig
    email: EmailConfig
    logging: LoggingConfig = LoggingConfig()

    model_config = SettingsConfigDict(
        extra="ignore",
        populate_by_name=True,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=str(BASEDIR / ".env"),
    )


settings = Config()  # ty: ignore[missing-argument]
