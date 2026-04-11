from dataclasses import dataclass

from application.dto import CreateLikeDTO
from application.interfaces.gateways import CacheService
from application.interfaces.repositories import LikeRepository
from application.interfaces.unit_of_work import UnitOfWork
from domain.entities import Like


def reaction_cache_key(video_id: int, reaction_type: str) -> str:
    return f"videos:{video_id}:{reaction_type}"


async def get_cached_count(
    cache: CacheService,
    repo: LikeRepository,
    video_id: int,
    reaction_type: str,
) -> int:
    cached = await cache.get(reaction_cache_key(video_id, reaction_type))
    if cached is not None:
        return int(cached)

    count = (
        await repo.count_likes(video_id)
        if reaction_type == "like"
        else await repo.count_dislikes(video_id)
    )
    await cache.set(reaction_cache_key(video_id, reaction_type), str(count), ttl=600)
    return count


async def set_cached_count(
    cache: CacheService,
    video_id: int,
    reaction_type: str,
    count: int,
) -> None:
    await cache.set(reaction_cache_key(video_id, reaction_type), str(count), ttl=600)


@dataclass
class SetReactionInteractor:
    _like_repository: LikeRepository
    _cache_service: CacheService
    _uow: UnitOfWork

    async def execute(self, data: CreateLikeDTO) -> bool:
        async with self._uow:
            existing = await self._like_repository.find_by_user_and_video(data.user_id, data.video_id)

            likes_count = await get_cached_count(self._cache_service, self._like_repository, data.video_id, "like")
            dislikes_count = await get_cached_count(self._cache_service, self._like_repository, data.video_id, "dislike")

            if existing:
                if existing.is_like == data.is_like:
                    await self._like_repository.delete(existing.id)
                    if data.is_like:
                        await set_cached_count(self._cache_service, data.video_id, "like", likes_count - 1)
                    else:
                        await set_cached_count(self._cache_service, data.video_id, "dislike", dislikes_count - 1)
                    return True
                existing.is_like = data.is_like
                await self._like_repository.update(existing)
                if data.is_like:
                    await set_cached_count(self._cache_service, data.video_id, "like", likes_count + 1)
                    await set_cached_count(self._cache_service, data.video_id, "dislike", dislikes_count - 1)
                else:
                    await set_cached_count(self._cache_service, data.video_id, "like", likes_count - 1)
                    await set_cached_count(self._cache_service, data.video_id, "dislike", dislikes_count + 1)
                return True
            like = Like(
                id=None,
                user_id=data.user_id,
                video_id=data.video_id,
                is_like=data.is_like,
            )
            await self._like_repository.create(like)
            if data.is_like:
                await set_cached_count(self._cache_service, data.video_id, "like", likes_count + 1)
            else:
                await set_cached_count(self._cache_service, data.video_id, "dislike", dislikes_count + 1)
            return True


@dataclass
class GetLikeStatsInteractor:
    _like_repository: LikeRepository
    _cache_service: CacheService

    async def execute(self, video_id: int, user_id: int | None = None) -> dict:
        likes_count = await get_cached_count(self._cache_service, self._like_repository, video_id, "like")
        dislikes_count = await get_cached_count(self._cache_service, self._like_repository, video_id, "dislike")

        user_reaction = None
        if user_id:
            user_reaction = await self._like_repository.get_user_reaction(video_id, user_id)

        return {
            "video_id": video_id,
            "likes_count": likes_count,
            "dislikes_count": dislikes_count,
            "user_reaction": user_reaction,
        }
