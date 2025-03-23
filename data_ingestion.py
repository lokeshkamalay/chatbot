import api.utils.chroma_utils as chroma_utils
import os
import api.utils.db_utils as db_utils
for file in os.listdir("docs"):
    if file.endswith(".md"):
        file_path = os.path.join("docs", file)
        print(f"Processing file: {file_path}")
        file_id = db_utils.insert_document_record(file)
        chroma_utils.index_document_to_chroma(file_path, file_id)

### from chatgpt it is not working effectively ignoring this
# import os
# import glob
# import markdown
# from bs4 import BeautifulSoup
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document

# # ChromaDB Configurations
# VECTORDATABASE_PATH = "vectors/chroma_db2"
# EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# # EMBEDDING_MODEL = "sentence-transformers/multi-qa-mpnet-base-dot-v1"


# # Initialize Embeddings & Vector Store
# embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
# vectorstore = Chroma(persist_directory=VECTORDATABASE_PATH, embedding_function=embedding_function)

# # Load and Process Markdown Files
# MARKDOWN_DIR = "./docs"  # Change to your markdown files directory
# markdown_files = glob.glob(os.path.join(MARKDOWN_DIR, "*.md"))

# def extract_content_from_markdown(md_text):
#     """Parses markdown content to extract headers and steps."""
#     html = markdown.markdown(md_text)  # Convert Markdown to HTML
#     soup = BeautifulSoup(html, "html.parser")

#     sections = []
#     current_header = None
#     steps = []

#     for tag in soup.find_all(["h1", "h2", "h3", "p", "ul", "ol", "code"]):
#         if tag.name in ["h1", "h2", "h3"]:
#             if current_header:  
#                 sections.append({"header": current_header, "steps": "\n".join(steps)})
#                 steps = []  
#             current_header = tag.get_text()
#         else:
#             steps.append(tag.get_text())

#     if current_header:
#         sections.append({"header": current_header, "steps": "\n".join(steps)})

#     return sections

# def index_markdown_to_chroma():
#     """Indexes extracted markdown data into ChromaDB."""
#     for md_file in markdown_files:
#         with open(md_file, "r", encoding="utf-8") as file:
#             md_content = file.read()
        
#         sections = extract_content_from_markdown(md_content)

#         documents = []
#         metadatas = []

#         for section in sections:
#             doc_text = f"## {section['header']}\n{section['steps']}"
#             # documents.append(Document(page_content=doc_text))
#             documents.append(Document(page_content=doc_text, metadata={"header": section["header"], "source_file": md_file}))
#             # metadatas.append({"header": section["header"], "source_file": md_file})

#         # Add documents to ChromaDB
#         # vectorstore.add_documents(documents, metadatas=metadatas)
#         vectorstore.add_documents(documents)
#         print(f"Ingested: {md_file} ✅")

#     # vectorstore.persist()  # Save the database
#     print("✅ Data ingestion completed!")

# # Run ingestion
# index_markdown_to_chroma()
