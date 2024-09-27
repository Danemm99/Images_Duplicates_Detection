from fastapi import APIRouter
from apps.api.images_api import routes as images_routes


api_router = APIRouter()


api_router.include_router(images_routes.router, tags=["images"])
