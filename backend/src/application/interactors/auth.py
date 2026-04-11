import json
import time
import uuid
from dataclasses import dataclass

from application.dto import (
    AvatarPresignedUrlDTO,
    JwtTokenDTO,
    LoginUserDTO,
    RegisterUserDTO,
    UpdateAvatarDTO,
    UpdateUserProfileDTO,
    UserProfileDTO,
)
from application.events import UserCreatedEvent, UserLoggedInEvent, UserLoggedOutEvent
from application.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from application.interfaces.gateways import (
    CacheService,
    EventPublisher,
    JwtService,
    PasswordHasher,
    StorageService,
)
from application.interfaces.repositories import SubscriptionRepository, UserRepository
from application.interfaces.unit_of_work import UnitOfWork
from domain.entities import User
from infrastructure.resources.logging import get_logger

logger = get_logger(__name__)


@dataclass
class RegisterUserInteractor:
    _user_repository: UserRepository
    _password_hasher: PasswordHasher
    _jwt_service: JwtService
    _event_publisher: EventPublisher
    _uow: UnitOfWork

    async def execute(self, data: RegisterUserDTO) -> JwtTokenDTO:
        async with self._uow:
            existing_user = await self._user_repository.find_by_email(data.email)
            if existing_user:
                raise UserAlreadyExistsError("email", data.email)

            existing_user = await self._user_repository.find_by_username(data.username)
            if existing_user:
                raise UserAlreadyExistsError("username", data.username)

            hashed_password = self._password_hasher.hash(data.password)

            user = User(
                id=None,
                username=data.username,
                email=data.email,
                hashed_password=hashed_password,
                first_name=data.first_name,
                last_name=data.last_name,
            )

            user = await self._user_repository.create(user)

            token = self._jwt_service.create_token(
                payload={
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            )

            await self._event_publisher.publish(
                UserCreatedEvent(user_id=user.id, email=user.email, username=user.username),
            )

            return JwtTokenDTO(access_token=token)


@dataclass
class LoginUserInteractor:
    _user_repository: UserRepository
    _password_hasher: PasswordHasher
    _jwt_service: JwtService
    _event_publisher: EventPublisher

    async def execute(self, data: LoginUserDTO) -> JwtTokenDTO:
        user = await self._user_repository.find_by_email(data.email)
        if not user or not self._password_hasher.verify(data.password, user.hashed_password):
            raise InvalidCredentialsError

        token = self._jwt_service.create_token(
            payload={
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        )

        await self._event_publisher.publish(
            UserLoggedInEvent(user_id=user.id, email=user.email, username=user.username),
        )

        return JwtTokenDTO(access_token=token)


@dataclass
class LogoutUserInteractor:
    _cache_service: CacheService
    _jwt_service: JwtService
    _event_publisher: EventPublisher

    async def execute(self, token: str, user_id: int) -> None:
        try:
            payload = self._jwt_service.decode_token(token)
            ttl = int(payload["exp"] - time.time())
            await self._cache_service.set(token, "blacklisted", ttl=ttl)
        except Exception:
            pass

        await self._event_publisher.publish(UserLoggedOutEvent(user_id=user_id))


@dataclass
class EditUserProfileInteractor:
    _user_repository: UserRepository
    _subscription_repository: SubscriptionRepository
    _uow: UnitOfWork

    async def execute(self, user_id: int, data: UpdateUserProfileDTO) -> UserProfileDTO:
        async with self._uow:
            user = await self._user_repository.find_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            if data.email is not None and data.email != user.email:
                existing = await self._user_repository.find_by_email(data.email)
                if existing and existing.id != user_id:
                    raise UserAlreadyExistsError("email", data.email)
                user.email = data.email

            if data.username is not None and data.username != user.username:
                existing = await self._user_repository.find_by_username(data.username)
                if existing and existing.id != user_id:
                    raise UserAlreadyExistsError("username", data.username)
                user.username = data.username

            if data.first_name is not None:
                user.first_name = data.first_name
            if data.last_name is not None:
                user.last_name = data.last_name

            user = await self._user_repository.update(user)

            subscribers_count = await self._subscription_repository.count_subscribers(user_id)

            return UserProfileDTO(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                total_subscribers=subscribers_count,
                avatar=user.avatar_url,
            )


@dataclass
class GetUserProfileInteractor:
    _user_repository: UserRepository
    _subscription_repository: SubscriptionRepository

    async def execute(self, user_id: int) -> UserProfileDTO:
        user = await self._user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        subscribers_count = await self._subscription_repository.count_subscribers(user_id)

        return UserProfileDTO(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            total_subscribers=subscribers_count,
            avatar=user.avatar_url,
        )


@dataclass
class GetAvatarPresignedUrlInteractor:
    _storage_service: StorageService

    async def execute(self, user_id: int, content_type: str) -> AvatarPresignedUrlDTO:
        ext = content_type.split("/")[1]
        key = f"avatar/{user_id}/{uuid.uuid4()}.{ext}"
        presigned_url = await self._storage_service.generate_presigned_upload_url(
            key=key,
            content_type=content_type,
        )
        return AvatarPresignedUrlDTO(presigned_url=presigned_url, key=key)


@dataclass
class CreateWsTicketInteractor:
    _cache_service: CacheService

    async def execute(self, user_id: int) -> str:
        ticket = str(uuid.uuid4())
        await self._cache_service.set(f"ws_ticket:{ticket}", json.dumps({"user_id": str(user_id)}), ttl=30)
        return ticket


@dataclass
class UpdateAvatarInteractor:
    _user_repository: UserRepository
    _subscription_repository: SubscriptionRepository
    _storage_service: StorageService
    _uow: UnitOfWork

    async def execute(self, user_id: int, data: UpdateAvatarDTO) -> UserProfileDTO:
        async with self._uow:
            user = await self._user_repository.find_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            user.avatar_url = await self._storage_service.get_url(data.key)
            user = await self._user_repository.update(user)

            subscribers_count = await self._subscription_repository.count_subscribers(user_id)
            return UserProfileDTO(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                total_subscribers=subscribers_count,
                avatar=user.avatar_url,
            )
