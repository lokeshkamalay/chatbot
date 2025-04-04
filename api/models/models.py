from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List, Dict

class Status(BaseModel):    
    # This model defines the structure of the status response.
    #TODO: Need to add the connection status of the database and other services.
    message: str = "ok"

class ModelName(str, Enum):
    # Ensures only predefined values are used.
    # If you try to use a value that is not in the list, it will raise a ValueError.
    OLAMA_32 = "llama3.2"

class Message(BaseModel):
    role: str
    content: str
    avatar: str = None
    user: str

# class QueryInput(BaseModel):
#     username: str
#     messages: List[Dict[str, str]] = Field(default_factory=list)
#     session_id: str = Field(default=None)
#     model: ModelName = Field(default=ModelName.OLAMA_32)

class QueryInput(BaseModel):
    username: str
    messages: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.OLAMA_32)

class QueryResponse(BaseModel):
    # Defines the expected structure of an API response.
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    #Helps track uploaded documents with timestamps.
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int

class RequestUserSessions(BaseModel):
    username: str = Field(default=None) 

class SessionInfo(BaseModel):
    message: str
    session_id: str
    last_active: datetime

class ResponseUserSessions(BaseModel):
    sessions: List[SessionInfo] = Field(default_factory=list)

class RequestSessionChatHistory(BaseModel):
    session_id: str

class ResponseSessionChatHistory(BaseModel):
    messages: List[Dict[str, str]] = Field(default_factory=list)
