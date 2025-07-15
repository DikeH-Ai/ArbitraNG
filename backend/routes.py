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
from backend.db.models.listing import Listing, ListingWrite, ListingBase
# Product ORM + Pydantic read schema
from backend.db.models.product import Product, ProductRead, ProductCreate, ProductBase, ProductUpdate


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


# GET /products/{product_id}
@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, session: Session = Depends(get_session)):
    """
    Fetches a product and it's related listings using selectinload to
    avoid N+1 query problem.
    Returns a product.
    """
    # Execute SQLmodel query
    product = session.get(Product, product_id)

    # Not found ?
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/products/", response_model=ProductBase)  # POST /products/
async def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    """
    Creates a product.
    returns a product
    """
    # validate input
    db_product = Product.model_validate(product)

    # Add to database
    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


# PUT /products/{product_id}
@router.patch("/products/{product_id}", response_model=ProductBase)
async def update_product(product_id: int, product: ProductUpdate, session: Session = Depends(get_session)):
    """
    Update/Modify product
    """
    # Get product
    product_db = session.get(Product, product_id)
    # Not found ?
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    # serialize data & exclude default fields
    product_data = product.model_dump(exclude_unset=True)
    # Apply changes to database
    product_db.sqlmodel_update(product_data)
    session.add(product_db)
    session.commit()
    session.refresh(product_db)

    return product_db


@router.delete("/products/{product_id}")  # DELETE /product/{product_id}
async def delete_product(product_id: int, session: Session = Depends(get_session)) -> dict[str, bool]:
    """
    Delete Product from database
    """
    # Select product from database
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # remove from database
    session.delete(product)
    session.commit()

    return {"ok": True}


# Listing Endpoints

# GET /products/{product_id}/listings/
@router.get("/products/{product_id}/listings/", response_model=List[ListingBase])
async def get_product_listing(product_id: int, session: Session = Depends(get_session)):
    """
    Fetch all listings of a Product
    return listings
    """
    statement = select(Listing).where(Listing.product_id == product_id)
    # Execute SQLmodel query
    listings = session.exec(statement=statement)

    return listings


# POST /products/{product_id}/listings/
@router.post("/products/{product_id}/listings/", response_model=ListingBase)
async def create_product_listing(product_id: int, listing_in: ListingWrite, session: Session = Depends(get_session)):
    """
    Create listing using product_id as foreign_key
    """
    # verify the product exist
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # retrive json data
    listing_data = listing_in.model_dump()

    # Include product_id->foreign_key
    listing_data["product_id"] = product_id

    # Validate & create ORM object
    listing_ok = Listing.model_validate(listing_data)
    # Add to database
    session.add(listing_ok)
    session.commit()
    session.refresh(listing_ok)

    return listing_ok


@router.delete("/products/{listing_id}")
async def delete_listing(listing_id: int, session: Session = Depends(get_session)):
    """
    Deletes listing using listing_id->primary_key
    """
    # Get listing
    listing = session.get(Listing, listing_id)

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    # Remove from database
    session.delete(listing)
    session.commit()

    return {"ok": True}
