# Imports
from sqlmodel import SQLModel, Field
from enum import Enum


# MarketPlace Enum

class MarketPlace(str, Enum):
    """
    Enum for supported e-commerce platforms.
    Separates local vs. international marketplaces.
    """
    # Local marketplaces
    jumia = "Jumia"
    jiji = "Jiji"
    konga = "Konga"

    # International marketplaces
    aliexpress = "AliExpress"
    amazon = "Amazon"
    ebay = "Ebay"


# Listing ORM Model

class Listing(SQLModel, table=True):
    """
    ORM model for a product listing on a specific marketplace.
    Each listing belongs to one Product and includes pricing and link details.
    """
    id: int | None = Field(
        default=None,
        primary_key=True,
    )
    product_id: int | None = Field(  # remove None option during deployment
        foreign_key="product.id",
        ondelete="CASCADE"
    )
    marketplace: MarketPlace = Field(
        ...,
        description="Marketplace where this listing is found (e.g., Jumia, AliExpress)"
    )
    price: float = Field(
        ...,
        ge=0,
        description="Price of the product listing in Naira (must be >= 0)"
    )
    product_link: str = Field(
        ...,
        description="Fully-qualified URL to the seller's product page"
    )
    title: str = Field(
        ...,
        description="Title of the product listing"
    )
    image_url: str = Field(
        ...,
        description="URL of the product image"
    )

# ListingBase Schema


class ListingBase(SQLModel):
    """
    Pydantic schema for serializing Listing.
    """
    id: int
    product_id: int | None = None
    title: str
    marketplace: MarketPlace
    price: float
    image_url: str
    product_link: str


class ListingWrite(SQLModel):
    """
    Schema for creating listing
    """
    title: str
    marketplace: MarketPlace
    price: float
    image_url: str
    product_link: str
