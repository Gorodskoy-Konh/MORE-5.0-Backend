from fastapi import Depends

from app.api.dependencies.database import get_repository
from app.database.repositories.products import ProductsRepository
from app.schemas.models.offices import OfficeDto


async def get_products_dependency(
        products_repo: ProductsRepository = Depends(
            get_repository(ProductsRepository)
        ),
) -> list[OfficeDto]:
    return await products_repo.get_products()
