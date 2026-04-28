"""
MongoDB helper functions for DS 4320 Project 2.
"""

import os
import logging
from typing import List, Dict, Any

import certifi
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    filename="logs/project2_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_mongo_client() -> MongoClient:
    """Create and return a MongoDB client using the MONGO_URI environment variable."""
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("MONGO_URI is missing. Add it to your .env file.")

    return MongoClient(
        mongo_uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000
    )


def get_database(db_name: str = "masters_project"):
    """Return the MongoDB database object."""
    client = get_mongo_client()
    return client[db_name]


def dataframe_to_documents(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert a pandas DataFrame into MongoDB-ready documents."""
    return df.where(pd.notnull(df), None).to_dict(orient="records")


def rebuild_collection(db, collection_name: str, df: pd.DataFrame) -> int:
    """
    Clear a MongoDB collection and upload documents from a DataFrame.
    Returns the number of uploaded documents.
    """
    try:
        collection = db[collection_name]
        docs = dataframe_to_documents(df)

        collection.delete_many({})

        if docs:
            collection.insert_many(docs)

        count = collection.count_documents({})
        logging.info(f"Uploaded {count} documents to {collection_name}")
        return count

    except Exception as error:
        logging.exception(f"Failed to rebuild collection: {collection_name}")
        raise error
