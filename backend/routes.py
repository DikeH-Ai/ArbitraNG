# Imports

from backend.db.db_config import get_session  # Database session dependency
# ORM session + query builder
from sqlmodel import Session, select
# To eagerly load relationships (avoid N+1)
from sqlalchemy.orm import selectinload
# Type casting for relationship fields
from sqlalchemy.orm.attributes import InstrumentedAttribute
# FastAPI routing and dependencies
from fastapi import Depends, APIRouter, HTTPException
from typing import List, cast  # Type hints
# Listing ORM + Pydantic read schema
from backend.db.models.listing import Listing, ListingRead
# Product ORM + Pydantic read schema
from backend.db.models.product import Product, ProductRead


# Router Setup


router = APIRouter()


# Root Route (Health Check)


@router.get("/")  # GET /
async def get_root():
    return {"message": "Root"}


# Product Endpoints


@router.get("/products/", response_model=List[ProductRead])  # GET /products/
async def get_products(session: Session = Depends(get_session)):
    """
    Fetches all products and their related listings using selectinload
    to avoid the N+1 query problem.
    Returns a list of products serialized as ProductRead schemas.
    """

    # Use eager loading to fetch Product.listings in a single additional query
    statement = select(Product).options(
        # Cast for type safety
        selectinload(cast(InstrumentedAttribute, Product.listings))
    )

    # Execute the SQLModel query
    products = session.exec(statement).all()

    return products

# listing endpoints
