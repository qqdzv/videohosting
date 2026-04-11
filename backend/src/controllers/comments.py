from dataclasses import dataclass
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from application.dto import (
    CommentDTO,
    CreateCommentDTO,
    SuccessResponseDTO,
    UpdateCommentDTO,
)
from application.interactors.comments import (
    CreateCommentInteractor,
    DeleteCommentInteractor,
    EditCommentInteractor,
    GetCommentsForVideoInteractor,
)
from application.interfaces.id_provider import IdProvider
from controllers.dependencies import get_id_provider

router = APIRouter(tags=["Comments"])


@dataclass
class CreateCommentBody:
    text: str


@router.post("/videos/{video_id}/comments")
@inject
async def create_comment_route(
    data: CreateCommentBody,
    video_id: int,
    interactor: FromDishka[CreateCommentInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()
    dto = CreateCommentDTO(video_id=video_id, author_id=user_id, text=data.text)
    await interactor.execute(data=dto)
    return SuccessResponseDTO()


@router.delete("/comments/{comment_id}", status_code=202)
@inject
async def delete_comment_route(
    comment_id: int,
    interactor: FromDishka[DeleteCommentInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()
    await interactor.execute(comment_id=comment_id, user_id=user_id)
    return SuccessResponseDTO()


@router.patch("/comments/{comment_id}")
@inject
async def edit_comment_route(
    comment_id: int,
    data: UpdateCommentDTO,
    interactor: FromDishka[EditCommentInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()
    await interactor.execute(comment_id=comment_id, user_id=user_id, data=data)
    return SuccessResponseDTO()


@router.get("/videos/{video_id}/comments")
@inject
async def get_comment_route(
    video_id: int,
    interactor: FromDishka[GetCommentsForVideoInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> list[CommentDTO]:
    id_provider.get_current_user_id()
    return await interactor.execute(video_id=video_id)
