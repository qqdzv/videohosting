import json
from dataclasses import dataclass
from typing import ClassVar

from application.dto import AuthorDTO
from application.events import SubscriptionCreatedEvent
from application.exceptions import SelfSubscriptionError
from application.interfaces.gateways import CacheService, EventPublisher
from application.interfaces.repositories import SubscriptionRepository, UserRepository
from application.interfaces.unit_of_work import UnitOfWork
from domain.entities import Subscription
from infrastructure.resources.logging import get_logger

logger = get_logger(__name__)


@dataclass
class SubscribeToUserInteractor:
    _subscription_repository: SubscriptionRepository
    _user_repository: UserRepository
    _event_publisher: EventPublisher
    _cache_service: CacheService
    _uow: UnitOfWork

    async def execute(self, subscriber_id: int, author_username: str) -> bool:
        async with self._uow:
            author = await self._user_repository.find_by_username(author_username)
            if not author:
                return False

            if subscriber_id == author.id:
                raise SelfSubscriptionError

            existing = await self._subscription_repository.find_by_subscriber_and_author(
                subscriber_id, author.id,
            )
            if existing:
                return False

            subscription = Subscription(
                id=None,
                subscriber_id=subscriber_id,
                author_id=author.id,
            )
            await self._subscription_repository.create(subscription)

            await self._cache_service.delete(
                f"{GetMySubscriptionsInteractor.CACHE_KEY_PREFIX}:{subscriber_id}",
            )

            subscriber = await self._user_repository.find_by_id(subscriber_id)
            await self._event_publisher.publish(
                SubscriptionCreatedEvent(
                    user_id=author.id,
                    email=author.email,
                    username=author.username,
                    follower=subscriber.username,
                ),
            )

            return True


@dataclass
class UnsubscribeFromUserInteractor:
    _subscription_repository: SubscriptionRepository
    _user_repository: UserRepository
    _cache_service: CacheService
    _uow: UnitOfWork

    async def execute(self, subscriber_id: int, author_username: str) -> bool:
        async with self._uow:
            author = await self._user_repository.find_by_username(author_username)
            if not author:
                return False

            subscription = await self._subscription_repository.find_by_subscriber_and_author(
                subscriber_id, author.id,
            )
            if not subscription:
                return False

            await self._subscription_repository.delete(subscription.id)

            await self._cache_service.delete(
                f"{GetMySubscriptionsInteractor.CACHE_KEY_PREFIX}:{subscriber_id}",
            )

            return True


@dataclass
class SearchUsersInteractor:
    _user_repository: UserRepository
    _subscription_repository: SubscriptionRepository

    async def execute(self, query: str) -> list[AuthorDTO]:
        users = await self._user_repository.search_by_username(query)

        result = []
        for user in users:
            subscribers_count = await self._subscription_repository.count_subscribers(user.id)
            result.append(
                AuthorDTO(
                    id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    avatar=user.avatar_url,
                    total_subscribers=subscribers_count,
                ),
            )

        return result


@dataclass
class CheckSubscriptionStatusInteractor:
    _subscription_repository: SubscriptionRepository
    _user_repository: UserRepository

    async def execute(self, subscriber_id: int, author_username: str) -> bool:
        author = await self._user_repository.find_by_username(author_username)
        if not author:
            return False

        subscription = await self._subscription_repository.find_by_subscriber_and_author(
            subscriber_id, author.id,
        )
        return subscription is not None


@dataclass
class GetMySubscriptionsInteractor:
    _subscription_repository: SubscriptionRepository
    _user_repository: UserRepository
    _cache_service: CacheService

    CACHE_TTL: ClassVar[int] = 60
    CACHE_KEY_PREFIX: ClassVar[str] = "my_subscriptions"

    async def execute(self, user_id: int) -> list[AuthorDTO]:
        cache_key = f"{self.CACHE_KEY_PREFIX}:{user_id}"

        cached = await self._cache_service.get(cache_key)
        if cached:
            return [AuthorDTO(**item) for item in json.loads(cached)]

        subscriptions = await self._subscription_repository.find_by_subscriber(user_id)

        result = []
        for subscription in subscriptions:
            author = await self._user_repository.find_by_id(subscription.author_id)
            if author:
                subscribers_count = await self._subscription_repository.count_subscribers(author.id)
                result.append(
                    AuthorDTO(
                        id=author.id,
                        username=author.username,
                        first_name=author.first_name,
                        last_name=author.last_name,
                        avatar=author.avatar_url,
                        total_subscribers=subscribers_count,
                    ),
                )

        await self._cache_service.set(
            cache_key,
            json.dumps([item.__dict__ for item in result]),
            ttl=self.CACHE_TTL,
        )

        return result


@dataclass
class GetAllChannelsInteractor:
    _user_repository: UserRepository
    _subscription_repository: SubscriptionRepository

    async def execute(self) -> list[AuthorDTO]:
        users = await self._user_repository.find_all()

        result = []
        for user in users:
            subscribers_count = await self._subscription_repository.count_subscribers(user.id)
            result.append(
                AuthorDTO(
                    id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    avatar=user.avatar_url,
                    total_subscribers=subscribers_count,
                ),
            )

        return result
