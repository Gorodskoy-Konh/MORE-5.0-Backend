from fastapi import Depends

from app.api.dependencies.database import get_repository
from app.database.error import BadRequestError
from app.database.repositories import orders
