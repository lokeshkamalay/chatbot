from fastapi import FastAPI
import structlog
import logging
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import status, chat

logger = structlog.getLogger(__name__)
app = FastAPI(
    title="lokeshfastapi", description="just a test repo", version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def docs_reroute() -> RedirectResponse:
    """
    Redirects the root URL to the FastAPI documentation.
    """
    return RedirectResponse(url="/docs")

app.include_router(status.router, prefix="/api/v1", tags=["status"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])