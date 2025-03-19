from typing import Any, Annotated
from fastapi import APIRouter, Depends, Request
from services.status_service import StatusService
from models.models import Status


router = APIRouter()

def get_status_service() -> StatusService:
    return StatusService()

@router.get("/status")
async def status(
    request: Request,
    service: Annotated[StatusService, Depends(get_status_service)],
) -> Status:
    """
    Returns the status of the application.
    """
    return service.get_status()

