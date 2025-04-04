import api.utils.chroma_utils as chroma_utils
import os
import api.utils.db_utils as db_utils

for file in os.listdir("docs"):
    if file.endswith(".md"):
        file_path = os.path.join("docs", file)
        print(f"Processing file: {file_path}")
        file_id = db_utils.insert_document_record(file)
        chroma_utils.index_document_to_chroma(file_path, file_id)
