from fastapi import Depends

from app.api.dependencies.database import get_repository
from app.database.error import BadRequestError
from app.database.repositories.offices import ATMsRepository
from app.schemas.models.atm import ATMDto, GetATMsDto


async def get_atms_dependency(
    get_atms_request: GetATMsDto = Depends(),
    atms_repo: ATMsRepository = Depends(
        get_repository(ATMsRepository)
    ),
) -> list[ATMDto]:
    if get_atms_request.radius and not (get_atms_request.longitude and get_atms_request.latitude):
        raise BadRequestError()
    return await atms_repo.get_atms(get_atms=get_atms_request)
