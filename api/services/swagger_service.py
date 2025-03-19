import os
import json
import httpx
import structlog
from pydantic import BaseModel
from models.models import Status
from typing import Any
from fastapi import Request

logger = structlog.getLogger(__name__)
class SwaggerService(BaseModel):
    async def get_swagger(self, request: Request) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{request.url.scheme}://{request.url.netloc}/openapi.json"
            )
            response.raise_for_status()
        swagger = response.json()
        if os.getenv("ENV") == "local":
            with open("./api.json", "w") as file:
                json.dump(swagger, file, indent=4)
        logger.info("Swagger Retrieved! \u2705")
        return swagger