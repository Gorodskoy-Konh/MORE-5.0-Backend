from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies.atms import get_atms_dependency
from app.schemas.models.atm import ATMDto
from app.schemas.responses.atms import GetATMsResponse

router = APIRouter(tags=["ATM-controller"], prefix='/atms')


@router.get(
    '/',
    name="atms::get-atms",
    operation_id="getATMs",
    status_code=status.HTTP_200_OK,
    response_model=GetATMsResponse,
    responses={
        status.HTTP_200_OK: {
            "model": GetATMsResponse,
            "description": "ok",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "bad request",
        }
    },
    tags=["ATM-controller"]
)
async def get_atms(
    atms: list[ATMDto] = Depends(get_atms_dependency)
):
    return GetATMsResponse(atms=atms)
