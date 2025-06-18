from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

# Avoid circular imports
if TYPE_CHECKING:
    from .listing import Listing
# Product schema: define product model


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    category: str | None = None
    image_url: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    listings: list["Listing"] = Relationship(back_populates="product")
