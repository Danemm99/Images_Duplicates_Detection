from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from dotenv import load_dotenv


load_dotenv()


client = QdrantClient(host=os.getenv("QDRANT_HOST"), port=os.getenv("QDRANT_PORT"), timeout=60)
collection_name = os.getenv("COLLECTION_NAME")


def create_collection():
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1000, distance=Distance.COSINE)
        )
