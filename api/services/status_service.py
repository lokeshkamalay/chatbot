import structlog
from pydantic import BaseModel
from models.models import Status

logger = structlog.getLogger(__name__)


class StatusService(BaseModel):
    def get_status(self) -> Status:
        logger.info("Getting Status......")
        status = Status(message="ok")
        logger.info("Status Retrieved! \u2705")
        return status