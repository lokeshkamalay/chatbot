from typing import List, Dict
import structlog
from pydantic import BaseModel
from models.models import QueryInput, QueryResponse
import utils.langchain_utils as langchain_utils
import ollama

logger = structlog.getLogger(__name__)


class ChatService(BaseModel):
    def chat_with_llama(self, messages: List[Dict[str, str]] = None):
        formatted_messages = [langchain_utils.format_message(m) for m in messages]
        response = ollama.chat(model='llama3.2', stream=True, messages=formatted_messages)
        full_message = ""
        for partial_resp in response:
            token = partial_resp["message"]["content"]
            full_message += token
            yield token
        return full_message

    def get_rag_chain(self, model_name: str) -> str:
        """Get the RAG chain for a specific model."""
        rag_chain = langchain_utils.get_rag_chain()
        return rag_chain