from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies.offices import get_offices_dependency, get_best_office_ids_dependency
from app.schemas.models.offices import OfficeDto
from app.schemas.responses.offices import GetOfficesResponse, GetBestOfficesResponse

# from app.api.dependencies.couriers import (
#     create_courier_dependency,
# )

router = APIRouter(tags=["office-controller"], prefix="/offices")


@router.get(
    "/",
    name="offices::get-offices",
    operation_id="getOffices",
    status_code=status.HTTP_200_OK,
    response_model=GetOfficesResponse,
    responses={
        status.HTTP_200_OK: {
            "model": GetOfficesResponse,
            "description": "ok",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "bad request",
        },
    },
    tags=["courier-controller"],
)
async def add_couriers(
    offices: list[OfficeDto] = Depends(get_offices_dependency)
        # create_courier_dependency
):
    return GetOfficesResponse(offices=offices)


@router.get(
    "/best",
    name="offices::get-best-offices",
    operation_id="getBestOffices",
    status_code=status.HTTP_200_OK,
    response_model=GetBestOfficesResponse,
    responses={
        status.HTTP_200_OK: {
            "model": GetBestOfficesResponse,
            "description": "ok",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "bad request",
        },
    },
    tags=["courier-controller"],
)
async def add_couriers(
    offices: list[int] = Depends(get_best_office_ids_dependency)
):
    return GetBestOfficesResponse(best_time=offices[0], closest=offices[1])
