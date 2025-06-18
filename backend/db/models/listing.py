from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
# e-commerce websites: select marketplace


class MarketPlace(str, Enum):
    # Local
    jumia = "Jumia"
    jiji = "Jiji"
    konga = "Konga"

    # Foreign
    aliexpress = "AliExpress"
    amazon = "Amazon"
    ebay = "Ebay"

# Store listings: product listings


class Listing(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    marketplace: MarketPlace
    price: float
    product_link: str

    product: "Product" = Relationship(back_populates="listings")
