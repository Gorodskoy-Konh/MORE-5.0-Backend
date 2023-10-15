from datetime import datetime

from pydantic import BaseModel


class CreateTicket(BaseModel):
    office_id: int
    product_name: str
    issue_time: datetime
