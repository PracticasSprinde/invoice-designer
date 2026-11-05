from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal


class ProductCreate(BaseModel):
    code: str | None = Field(default=None, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=250)
    category: str | None = Field(default=None, max_length=50)
    unit_price: Decimal = Field(ge=0)
    tax_rate: Decimal = Field(default=Decimal("21"), ge=0, le=100)

    user_id: int


class Product(ProductCreate):
    product_id: int
    model_config = ConfigDict(from_attributes=True)
