from fastapi import FastAPI, File, UploadFile, APIRouter
from typing import List
import uuid
from apps.crud.crud_images import crud_images


router = APIRouter()


@router.post("/images")
async def add_images(files: List[UploadFile] = File(...)):
    request_id = str(uuid.uuid4())
    return crud_images.add_images(files, request_id)


@router.get("/duplicates/{request_id}")
async def find_duplicates(request_id: str):
    return crud_images.find_duplicates(request_id)
