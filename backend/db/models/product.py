# Imports & Forward References
from sqlmodel import SQLModel, Field, Relationship  # Core SQLModel classes
from datetime import datetime, timezone            # Timestamp handling
# Type hints & avoiding circular imports
from typing import TYPE_CHECKING, List
from .listing import Listing, ListingRead

# Avoid circular imports by importing during type checking only
if TYPE_CHECKING:
    from .listing import Listing, ListingRead     # Used only for type annotations


# Product ORM Model


class Product(SQLModel, table=True):
    """
    ORM model for products.
    Represents a unique electronics product (e.g., "iPhone X 128GB").
    """
    id: int | None = Field(
        default=None,
        primary_key=True,
    )
    title: str = Field(
        ...,
        description="Normalized product title (e.g., 'Samsung Galaxy Tab A7')"
    )
    category: str | None = Field(
        default=None,
    )
    image_url: str = Field(
        ...,
        description="URL to a representative product image"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    # Relationship to listings: one product can have many listings
    listings: List["Listing"] = Relationship()


# ProductRead Pydantic Schema

class ProductRead(SQLModel):
    """
    Pydantic schema for serializing Product responses.
    Includes nested listings as ListingRead.
    """
    id: int
    title: str
    category: str | None
    image_url: str
    created_at: datetime
    # Nested Pydantic schema for related listings
    listings: List[ListingRead]
