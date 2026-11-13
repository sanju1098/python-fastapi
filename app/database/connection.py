
import os
from dotenv import load_dotenv
from fastapi import Request
from pymongo import AsyncMongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")


async def connect_to_mongodb(app):
    if not MONGODB_URL:
        raise RuntimeError("MONGODB_URL is not configured")

    if not DATABASE_NAME:
        raise RuntimeError("DATABASE_NAME is not configured")

    client = AsyncMongoClient(MONGODB_URL)

    try:
        await client.admin.command("ping")

        app.state.mongodb_client = client
        app.state.database = client[DATABASE_NAME]

        print("Connected to MongoDB successfully!")

    except Exception:
        await client.close()
        raise


async def close_mongodb_connection(app):
    client = getattr(app.state, "mongodb_client", None)

    if client:
        await client.close()
        print("MongoDB connection closed!")


def get_database(request: Request):
    return request.app.state.database
