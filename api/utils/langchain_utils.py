from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
import ollama
from utils.chroma_utils import vectorstore
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama 
from dotenv import load_dotenv
import os
from langchain_core.runnables import RunnableLambda
load_dotenv()

# retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
retriever = vectorstore.as_retriever(
    search_type='similarity_score_threshold',
    search_kwargs={"k": 3, "score_threshold": 0.5},
)

# retriever = vectorstore.as_retriever(
#     search_type='mmr',
#     search_kwargs={"k": 3, "fetch_k": 20, "lambda_mult": 0.5},
# )


output_parser = StrOutputParser()

# Set up prompts and chains
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Answer the question if you are aware, "
    "but do not include any personal information data that impacts user privacy. "
)


contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("user", "{input}"),
])

def format_message(message):
    if not message.get("system"):
        message['system'] = SystemMessage(content=contextualize_q_system_prompt)
    return message
#("system", "You are a helpful AI assistant. Use the following context to answer the user's question. Answer the question if you are aware but don't include any additional information apart from context.  If you don't know the answer, say 'I don't know'."),
qa_prompt_system = """
    You are a helpful AI assistant.
    Use the following context to answer the user's question. 
    Answer the question if you are aware but don't include any additional information apart from context.
    If the question is not clear, ask the user to clarify.
    If you don't know the answer, say 'I don't know'.
    """
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_prompt_system),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

def chat_with_llama(messages: List[Document] = None):
    formatted_messages = [format_message(m) for m in messages]
    response = ollama.chat(model='llama3.2', stream=True, messages=formatted_messages)
    full_message = ""
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        full_message += token
        yield token
    return full_message

def get_rag_chain():
    llm = ChatOllama(model='llama3.2', stream=True, temperature=0, max_tokens=2000, top_p=0.1)
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain
# How to convert maven github actions to cloudsmith
