from fastapi import Depends

from app.api.dependencies.database import get_repository
from app.database.error import BadRequestError
from app.database.repositories.offices import OfficesRepository
from app.schemas.models.offices import OfficeDto
from app.schemas.requests.offices import GetOfficesDto, GetBestOfficesDto


async def get_offices_dependency(
        get_offices_request: GetOfficesDto = Depends(),
        offices_repo: OfficesRepository = Depends(
            get_repository(OfficesRepository)
        ),
) -> list[OfficeDto]:
    if get_offices_request.radius and not (get_offices_request.longitude and get_offices_request.latitude):
        raise BadRequestError()
    return await offices_repo.get_offices(get_offices=get_offices_request)


async def get_best_office_ids_dependency(
        get_best_offices_request: GetBestOfficesDto = Depends(),
        offices_repo: OfficesRepository = Depends(
            get_repository(OfficesRepository)
        ),
) -> list[int]:
    return await offices_repo.get_best_offices(get_best_offices=get_best_offices_request)
