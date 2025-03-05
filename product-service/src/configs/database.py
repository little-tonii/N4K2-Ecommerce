from ..configs.variables import DATABASE_NAME, DATABASE_URL
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

client = AsyncIOMotorClient(DATABASE_URL)
database = client[DATABASE_NAME]

category_collection = database["categories"]
product_collection = database["products"]

async def get_db() -> AsyncIOMotorDatabase:
    return database