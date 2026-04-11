from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from application.dto import CreateLikeDTO, SetReactionDTO, SuccessResponseDTO
from application.interactors.likes import SetReactionInteractor
from application.interfaces.id_provider import IdProvider
from controllers.dependencies import get_id_provider

router = APIRouter(tags=["Likes"])


@router.post("/videos/{video_id}/likes")
@inject
async def set_like_route(
    video_id: int,
    data: SetReactionDTO,
    interactor: FromDishka[SetReactionInteractor],
    id_provider: Annotated[IdProvider, Depends(get_id_provider)],
) -> SuccessResponseDTO:
    user_id = id_provider.get_current_user_id()

    dto = CreateLikeDTO(
        video_id=video_id,
        user_id=user_id,
        is_like=(data.reaction == "like"),
    )
    await interactor.execute(data=dto)
    return SuccessResponseDTO()
