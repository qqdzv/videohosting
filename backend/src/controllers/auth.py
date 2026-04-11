from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Cookie, Depends, Query, Response

from application.dto import (
    AvatarPresignedUrlDTO,
    LoginUserDTO,
    RegisterUserDTO,
    SuccessResponseDTO,
    UpdateAvatarDTO,
    UpdateUserProfileDTO,
    UserProfileDTO,
)
from application.interactors.auth import (
    CreateWsTicketInteractor,
    EditUserProfileInteractor,
    GetAvatarPresignedUrlInteractor,
    GetUserProfileInteractor,
    LoginUserInteractor,
    LogoutUserInteractor,
    RegisterUserInteractor,
    UpdateAvatarInteractor,
)
from application.interfaces.id_provider import IdProvider
from controllers.dependencies import get_id_provider

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
@inject
async def login_route(
    data: LoginUserDTO,
    response: Response,
    interactor: FromDishka[LoginUserInteractor],
) -> SuccessResponseDTO:
    result = await interactor.execute(data)
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        secure=False, # False так как http
        samesite="lax",
    )
    return SuccessResponseDTO()


@router.post("/register")
@inject
async def register_route(
    data: RegisterUserDTO,
    response: Response,
    interactor: FromDishka[RegisterUserInteractor],
) -> SuccessResponseDTO:
    result = await interactor.execute(data)
    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        secure=False, # False так как http
        samesite="lax",
    )
    return SuccessResponseDTO()


@router.post("/logout")
@inject
async def logout_route(
    response: Response,
    interactor: FromDishka[LogoutUserInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
    access_token: Annotated[str | None, Cookie()] = None,
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()
    await interactor.execute(token=access_token or "", user_id=user_id)
    response.delete_cookie(key="access_token")
    return SuccessResponseDTO()


@router.patch("/profile")
@inject
async def edit_profile_route(
    data: UpdateUserProfileDTO,
    interactor: FromDishka[EditUserProfileInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> UserProfileDTO:
    user_id = id_provider.get_current_user_id()
    return await interactor.execute(user_id=user_id, data=data)


@router.get("/profile")
@inject
async def profile_route(
    interactor: FromDishka[GetUserProfileInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> UserProfileDTO:
    user_id = id_provider.get_current_user_id()
    return await interactor.execute(user_id=user_id)


@router.get("/ws-ticket")
@inject
async def get_ws_ticket_route(
    interactor: FromDishka[CreateWsTicketInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> dict[str, str]:
    user_id = id_provider.get_current_user_id()
    ticket = await interactor.execute(user_id=user_id)
    return {"ticket": ticket}


@router.get("/profile/avatar/presigned-url")
@inject
async def get_avatar_presigned_url_route(
    interactor: FromDishka[GetAvatarPresignedUrlInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
    content_type: str = Query(default="image/jpeg"),
) -> AvatarPresignedUrlDTO:
    user_id = id_provider.get_current_user_id()
    return await interactor.execute(user_id=user_id, content_type=content_type)


@router.patch("/profile/avatar")
@inject
async def update_avatar_route(
    data: UpdateAvatarDTO,
    interactor: FromDishka[UpdateAvatarInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> UserProfileDTO:
    user_id = id_provider.get_current_user_id()
    return await interactor.execute(user_id=user_id, data=data)
