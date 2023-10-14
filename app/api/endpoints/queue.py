from fastapi import APIRouter
from starlette import status

from app.database.models.tickets import TicketDB

router = APIRouter(tags=[], prefix="/queues")


@router.get(
    "/",
    name="queue::get-queues",
    operation_id="getQueues",
    status_code=status.HTTP_200_OK
)
async def get_queues(queues: list[TicketDB]):
    return queues


@router.post(
    "/"
)
async def add_to_queue(office_id, product_name):
    pass