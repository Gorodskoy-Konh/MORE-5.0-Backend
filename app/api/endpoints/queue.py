from fastapi import APIRouter, Depends, Query
from starlette import status

from app.database.models.order import OrderDB

router = APIRouter(tags=[], prefix="/queues")


@router.get(
    "/",
    name="queue::get-queues",
    operation_id="getQueues",
    status_code=status.HTTP_200_OK
)
async def get_queues(queues: list[OrderDB]):
    return queues


@router.post(
    "/"
)
async def add_to_queue(office_id, product_name):
    pass