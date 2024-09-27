from apps.main.config import client
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv
import pytest
import os


load_dotenv()


@pytest.fixture
def setup_qdrant():
    test_collection_name = os.getenv("TEST_COLLECTION_NAME")
    if not client.collection_exists(test_collection_name):
        client.create_collection(
            collection_name=test_collection_name,
            vectors_config=VectorParams(size=1000, distance=Distance.COSINE)
        )
    yield
    client.delete_collection(test_collection_name)
