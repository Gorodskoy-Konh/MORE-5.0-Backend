from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies.couriers import (
    create_courier_dependency,
)
from app.schemas.models.couriers import CourierDto
from app.schemas.responses.common import BadRequestResponse
from app.schemas.responses.couriers import (
    CreateCouriersResponse,
)

router = APIRouter(tags=["courier-controller"], prefix="/couriers")


@router.post(
    "/",
    name="couriers::add-couriers",
    operation_id="createCourier",
    status_code=status.HTTP_200_OK,
    response_model=CreateCouriersResponse,
    responses={
        status.HTTP_200_OK: {
            "model": CreateCouriersResponse,
            "description": "ok",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestResponse,
            "description": "bad request",
        },
    },
    tags=["courier-controller"],
)
async def add_couriers(
    couriers: list[CourierDto] = Depends(create_courier_dependency),
):
    return CreateCouriersResponse(couriers=couriers)
