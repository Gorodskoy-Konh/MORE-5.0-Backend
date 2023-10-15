from pydantic import BaseModel


class GetProductsResponse(BaseModel):
    products: list[str]
