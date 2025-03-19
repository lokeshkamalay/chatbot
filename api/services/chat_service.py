from typing import List, Dict
import structlog
from pydantic import BaseModel
from models.models import QueryInput, QueryResponse
from utils.langchain_utils import format_message
import ollama

logger = structlog.getLogger(__name__)


class ChatService(BaseModel):
    def chat_with_llama(self, messages: List[Dict[str, str]] = None):
        formatted_messages = [format_message(m) for m in messages]
        response = ollama.chat(model='llama3.2', stream=True, messages=formatted_messages)
        print(f"------------ {response} ------------")
        full_message = ""
        for partial_resp in response:
            token = partial_resp["message"]["content"]
            full_message += token
            yield token
        return full_message
