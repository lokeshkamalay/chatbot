import uuid
import structlog
from typing import Any, Annotated
from fastapi import APIRouter, Body, Depends, Request, HTTPException
from services.chat_service import ChatService
from models.models import QueryResponse, QueryInput
from pydantic import ValidationError
from fastapi.responses import StreamingResponse
import utils.db_utils as db_utils

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

    if not query_input.session_id:
        query_input.session_id = str(uuid.uuid4())
    db_utils.insert_chat_history(query_input.username, "user", query_input.session_id, query_input.messages)
    #logger.info(f"Session ID: {query_input.session_id}, User Query: {query_input.messages[:-1].get('content')}, Model: {query_input.model.value}")
    message_history = db_utils.get_chat_history(query_input.username, query_input.session_id)
    # async def response_generator():
    #     response_text = ""
    #     for chunk in service.chat_with_llama(message_history):
    #         response_text += chunk
    #         yield chunk
    #     # Save the complete response to a table (assuming you have a save_to_table function)
    #     db_utils.insert_chat_history(query_input.username, "assistant", query_input.session_id, response_text)

    # return StreamingResponse(response_generator(), media_type="text/plain", headers={"X-Session-ID": query_input.session_id})
    try:
        async def response_generator():
            rag_chain = service.get_rag_chain(query_input.model.value)
            response_text = ""
            async for chunk in rag_chain.astream({
                "input": query_input.messages,
                "chat_history": message_history
            }):
                if "answer" in chunk:  # Ensure 'answer' key exists
                    response_text += chunk["answer"]
                    yield chunk["answer"]
            db_utils.insert_chat_history(query_input.username, "assistant", query_input.session_id, response_text)
        return StreamingResponse(response_generator(), media_type="text/plain", headers={"X-Session-ID": query_input.session_id})
    except Exception as e:
        print(f"Error during chat processing:\n {e}")
    
    

    # response_text = ""
    # for chunk in service.chat_with_llama(query_input.messages):
    #     response_text += chunk
    # # response = service.chat_with_llama(query_input.messages)
    # print("************")
    # print(response_text)
    # return QueryResponse(answer=response_text, session_id=query_input.session_id, model=query_input.model)

