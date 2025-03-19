from typing import Any, Annotated
from fastapi import APIRouter, Depends, Request
from services.swagger_service import SwaggerService

router = APIRouter()

def get_swagger_service() -> SwaggerService:
    return SwaggerService()

@router.get("/swagger")
async def get_swagger(
    request: Request, service: Annotated[SwaggerService, Depends(get_swagger_service)]
) -> Any:
    return await service.get_swagger(request)