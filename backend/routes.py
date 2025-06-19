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
from backend.db.models.product import Product, ProductRead, ProductCreate, ProductBase


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


# GET /product/
@router.get("/product/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, session: Session = Depends(get_session)):
    """
    Fetches a product and it's related listings using selectinload to
    avoid N+1 query problem.
    Returns a product.
    """
    # select product by product id
    product = session.get(Product, product_id)

    # Not found ?
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/product/", response_model=ProductBase)  # POST /product/
async def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    """
    Creates a product.
    returns a product
    """
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product
