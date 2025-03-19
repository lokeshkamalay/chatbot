import uuid
import structlog
from typing import Any, Annotated
from fastapi import APIRouter, Body, Depends, Request, HTTPException
from services.chat_service import ChatService
from models.models import QueryResponse, QueryInput
from pydantic import ValidationError
from fastapi.responses import StreamingResponse

logger = structlog.getLogger(__name__)
router = APIRouter()

def get_chat_service() -> ChatService:
    return ChatService()

@router.post("/chat")
async def chat(
    service: Annotated[ChatService, Depends(get_chat_service)],
    query_input: Annotated[QueryInput, Body(...)]
) -> StreamingResponse:
    """
    Handles chat requests and returns the AI response.
    """

    print(query_input.messages)

    if not query_input.session_id:
        query_input.session_id = str(uuid.uuid4())
    #logger.info(f"Session ID: {query_input.session_id}, User Query: {query_input.messages[:-1].get('content')}, Model: {query_input.model.value}")
    async def response_generator():
        response_text = ""
        for chunk in service.chat_with_llama(query_input.messages):
            response_text += chunk
            yield chunk
        print("************")
        print(response_text)

    return StreamingResponse(response_generator(), media_type="text/plain")    
    
    # response_text = ""
    # for chunk in service.chat_with_llama(query_input.messages):
    #     response_text += chunk
    # # response = service.chat_with_llama(query_input.messages)
    # print("************")
    # print(response_text)
    # return QueryResponse(answer=response_text, session_id=query_input.session_id, model=query_input.model)

