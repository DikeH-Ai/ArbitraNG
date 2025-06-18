from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.db.db_config import create_database_and_tables
from backend.db.models.product import Product
from backend.db.models.listing import Listing
# remove during deployment


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database
    create_database_and_tables()
    print("Database schema created")
    yield


app = FastAPI(lifespan=lifespan)
