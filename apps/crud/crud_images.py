import os

from PIL import Image
import uuid
from qdrant_client.models import PointStruct, models
from typing import List
from apps.main.utils import image_to_vector
from apps.main.config import client, create_collection
from dotenv import load_dotenv


load_dotenv()


class CRUDImages:
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    SUPPORTED_FORMATS = ["image/jpeg", "image/png"]
    MAX_FILE_SIZE_MB = 10

    @classmethod
    def add_images(cls, files: List, request_id: str, collection_name=None) -> dict:
        if collection_name is None:
            collection_name = cls.COLLECTION_NAME
            create_collection()

        successful_uploads = 0

        for file in files:
            if file.content_type not in cls.SUPPORTED_FORMATS:
                return {"error": f"Unsupported file format: {file.content_type}. Only JPEG and PNG are allowed."}

            file_size_mb = file.size / (1024 * 1024)
            if file_size_mb > cls.MAX_FILE_SIZE_MB:
                return {"error": f"File {file.filename} is too large: {file_size_mb:.2f} MB. Max file size is {cls.MAX_FILE_SIZE_MB} MB."}

            image = Image.open(file.file)
            vector = image_to_vector(image)
            point_id = uuid.uuid4()

            url = f"http://example.com/images/{point_id}"
            filename = file.filename

            client.upsert(
                collection_name=collection_name,
                wait=True,
                points=[
                    PointStruct(id=str(point_id), vector=vector, payload={
                        "request_id": f"{request_id}",
                        "url": url,
                        "filename": filename,
                    }),
                ],
            )

            successful_uploads += 1

        response = {"request_id": request_id, "uploaded": successful_uploads}

        return response

    @classmethod
    def find_duplicates(cls, request_id: str, collection_name=None) -> dict:
        if collection_name is None:
            collection_name = cls.COLLECTION_NAME
            create_collection()

        search_results = client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                should=[
                    models.FieldCondition(
                        key="request_id", match=models.MatchValue(value=f"{request_id}")
                    ),
                ],
            ),
            with_vectors=True,
        )

        if not search_results:
            return {"message": "There isn't any vector for this request_id."}

        points = search_results[0]

        duplicates_id = []
        duplicates = []

        for point in points:
            if point.id in duplicates_id:
                continue

            query_vector = point.vector

            results = client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                score_threshold=0.85
            )

            if results:
                for result in results:
                    if result.id != point.id and result.id not in duplicates_id:
                        duplicates_id.append(result.id)
                        duplicates.append(result)

        if duplicates_id:
            return {
                "request_id": request_id,
                "duplicates": [
                    {
                        "image_id": elem.id,
                        "url": elem.payload.get("url"),
                        "filename": elem.payload.get("filename"),
                    } for elem in duplicates
                ]
            }

        return {"message": "Duplicates haven't been found."}


crud_images = CRUDImages()
