import uuid
import structlog
from typing import Any, Annotated
from fastapi import APIRouter, Body, Depends, Request, HTTPException
from services.chat_service import ChatService
from models.models import QueryResponse, QueryInput, ResponseUserSessions, ResponseSessionChatHistory
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
    # db_utils.insert_chat_history(query_input.username, "user", query_input.session_id, query_input.messages)
    # message_history = db_utils.get_chat_history(query_input.username, query_input.session_id)
    message_history = []
    
    # try:
    #     async def response_generator():
    #         rag_chain = service.get_rag_chain(query_input.model.value)
    #         response_text = ""
    #         async for chunk in rag_chain.astream({
    #             "input": query_input.messages,
    #             "chat_history": message_history
    #         }):
    #             if "answer" in chunk:  # Ensure 'answer' key exists
    #                 response_text += chunk["answer"]
    #                 yield chunk["answer"]
    #         # db_utils.insert_chat_history(query_input.username, "assistant", query_input.session_id, response_text)
    #     return StreamingResponse(response_generator(), media_type="text/plain", headers={"X-Session-ID": query_input.session_id})
    # except Exception as e:
    #     print(f"Error during chat processing:\n {e}")
    
    
    rag_chain = service.get_rag_chain(query_input.model.value)
    answer = rag_chain.invoke({
        "input": query_input.messages,
        "chat_history": message_history
    })
    print("========")
    print(type(answer))
    for document in answer["context"]:
        print(document)
        print()

    # print(f"Session ID: {query_input.session_id}, AI Response: {answer}")
    # return QueryResponse(answer=answer['answer'], session_id=query_input.session_id, model=query_input.model)

@router.get("/chat/usersessions/{username}", response_model=ResponseUserSessions)
async def get_user_sessions(
    username: str = None,
) -> ResponseUserSessions:
    """
    Retrieve chat history for a specific user and session.
    """
    try:
        # sessions = db_utils.get_user_sessions(username)
        sessions = []
        return ResponseUserSessions(sessions=sessions)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/chat/sessionhistory/{session_id}", response_model=ResponseSessionChatHistory)
async def get_session_messages(
    session_id: str,
) -> ResponseSessionChatHistory:
    """
    Retrieve chat messages for a specific session.
    """
    try:
        # messages = db_utils.get_session_messages(session_id)
        messages = []
        return ResponseSessionChatHistory(messages=messages)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
