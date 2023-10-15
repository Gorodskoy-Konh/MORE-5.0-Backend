from fastapi import APIRouter, Depends
from starlette import status

from app.api.dependencies.products import get_products_dependency
from app.schemas.responses.products import GetProductsResponse

router = APIRouter(tags=[], prefix="/products")


@router.get(
    "/",
    name="queue::get-products",
    operation_id="getProducts",
    status_code=status.HTTP_200_OK
)
async def get_products(products: list[str] = Depends(get_products_dependency)):
    return GetProductsResponse(products=products)
