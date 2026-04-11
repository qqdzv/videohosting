from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from application.dto import AuthorDTO, SuccessResponseDTO
from application.interactors.subscriptions import (
    CheckSubscriptionStatusInteractor,
    GetMySubscriptionsInteractor,
    SearchUsersInteractor,
    SubscribeToUserInteractor,
    UnsubscribeFromUserInteractor,
)
from application.interfaces.id_provider import IdProvider
from controllers.dependencies import get_id_provider

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/{follow_username}")
@inject
async def subscribe_route(
    follow_username: str,
    interactor: FromDishka[SubscribeToUserInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()

    status = await interactor.execute(subscriber_id=user_id, author_username=follow_username)
    return SuccessResponseDTO(success=status)


@router.delete("/{follow_username}")
@inject
async def unsubscribe_route(
    follow_username: str,
    interactor: FromDishka[UnsubscribeFromUserInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()

    status = await interactor.execute(subscriber_id=user_id, author_username=follow_username)
    return SuccessResponseDTO(success=status)


@router.get("/search")
@inject
async def search_users_route(
    interactor: FromDishka[SearchUsersInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
    query: str = "",
) -> list[AuthorDTO]:
    id_provider.get_current_user_id()

    return await interactor.execute(query=query)


@router.get("/{username}")
@inject
async def is_subscribed_route(
    username: str,
    interactor: FromDishka[CheckSubscriptionStatusInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()

    status = await interactor.execute(subscriber_id=user_id, author_username=username)
    return SuccessResponseDTO(success=status)


@router.get("")
@inject
async def my_subscriptions_route(
    interactor: FromDishka[GetMySubscriptionsInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> list[AuthorDTO]:
    user_id = id_provider.get_current_user_id()

    return await interactor.execute(user_id=user_id)
