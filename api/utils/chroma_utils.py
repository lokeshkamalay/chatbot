from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os

vectordb_path = "/Users/loki/Library/CloudStorage/GoogleDrive-lokesh.mydilse@gmail.com/My Drive/AA/MacPro/GenAI/Class28-chatbotfull/AA/vectors/chroma_db"
# vectordb_path = os.path.join(
#     os.getcwd(), "vectors", "chroma_db1"
# )

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
model_name = "sentence-transformers/all-MiniLM-L6-v2"
#sentence-transformers/multi-qa-mpnet-base-dot-v1 try this model as well

embedding_function = HuggingFaceEmbeddings(model_name=model_name)
vectorstore = Chroma(persist_directory=vectordb_path, embedding_function=embedding_function)

def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.html'):
        loader = UnstructuredHTMLLoader(file_path)
    elif file_path.endswith('.md'):
        print(f"Loading markdown file: {file_path}")
        loader = UnstructuredMarkdownLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    documents = loader.load()
    return text_splitter.split_documents(documents)

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)
        
        # Add metadata to each split
        metadata = {
            "source": file_path,
            "filename": os.path.basename(file_path),
            "file_id": file_id
        }
        for split in splits:
            # print(split)
            split.metadata = metadata
        
        vectorstore.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_chroma(file_id: int):
    try:
        docs = vectorstore.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")
        
        vectorstore._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")
        
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False
