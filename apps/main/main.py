from fastapi import FastAPI
from apps.api.routers import api_router


app = FastAPI(
    title="Images Duplicate Detection", openapi_url="/api/openapi.json"
)


app.include_router(api_router, prefix="/api")
