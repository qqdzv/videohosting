from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, UploadFile

from application.dto import (
    SuccessResponseDTO,
    UpdateVideoDTO,
    UploadFileResponseDTO,
    UploadVideoRequestDTO,
    VideoDetailDTO,
)
from application.interactors.media import (
    AddViewToVideoInteractor,
    DeleteVideoInteractor,
    EditVideoInteractor,
    GetUserHistoryInteractor,
    GetVideoByIdInteractor,
    GetVideoListInteractor,
    GetVideosByAuthorInteractor,
    SearchVideosInteractor,
    UploadVideoInteractor,
)
from application.interfaces.id_provider import IdProvider
from controllers.dependencies import get_id_provider

router = APIRouter(prefix="/videos", tags=["Media"])

@router.get("/search")
@inject
async def search_video_route(
    interactor: FromDishka[SearchVideosInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
    query: str = "",
) -> list[VideoDetailDTO]:
    user_id = id_provider.get_current_user_id()

    return await interactor.execute(query=query, user_id=user_id)


@router.get("/history")
@inject
async def get_history_route(
    interactor: FromDishka[GetUserHistoryInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> list[VideoDetailDTO]:
    user_id = id_provider.get_current_user_id()

    return await interactor.execute(user_id=user_id)


@router.get("/author/{author_username}")
@inject
async def get_videos_by_author_route(
    author_username: str,
    interactor: FromDishka[GetVideosByAuthorInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> list[VideoDetailDTO]:
    user_id = id_provider.get_current_user_id()

    return await interactor.execute(author_username=author_username, user_id=user_id)


@router.get("")
@inject
async def get_videos_route(
    interactor: FromDishka[GetVideoListInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
    offset: int = 0,
    limit: int = 100,
    is_random: bool = True,
) -> list[VideoDetailDTO]:
    user_id = id_provider.get_current_user_id()

    return await interactor.execute(user_id=user_id, offset=offset, limit=limit, is_random=is_random)


@router.post("")
@inject
async def upload_file_route(
    interactor: FromDishka[UploadVideoInteractor],
    file: UploadFile,
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
    title: str = "",
    description: str = "",
) -> UploadFileResponseDTO:
    user_id = id_provider.get_current_user_id()

    file_content = await file.read()
    dto = UploadVideoRequestDTO(
        title=title,
        description=description,
        file_content=file_content,
        filename=file.filename or "noname",
        content_type=file.content_type,
    )
    return await interactor.execute(data=dto, author_id=user_id)


@router.get("/{video_id}")
@inject
async def get_video_route(
    video_id: int,
    interactor: FromDishka[GetVideoByIdInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> VideoDetailDTO:
    user_id = id_provider.get_current_user_id()
    return await interactor.execute(video_id=video_id, user_id=user_id)


@router.post("/{video_id}/views")
@inject
async def add_view_route(
    video_id: int,
    interactor: FromDishka[AddViewToVideoInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()

    await interactor.execute(video_id=video_id, user_id=user_id)
    return SuccessResponseDTO()


@router.delete("/{video_id}", status_code=202)
@inject
async def delete_video_route(
    video_id: int,
    interactor: FromDishka[DeleteVideoInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()
    await interactor.execute(video_id=video_id, user_id=user_id)
    return SuccessResponseDTO()


@router.patch("/{video_id}")
@inject
async def edit_video_route(
    video_id: int,
    data: UpdateVideoDTO,
    interactor: FromDishka[EditVideoInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()
    await interactor.execute(video_id=video_id, user_id=user_id, data=data)
    return SuccessResponseDTO()
