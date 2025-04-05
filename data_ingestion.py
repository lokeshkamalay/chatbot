import api.utils.chroma_utils as chroma_utils
import os
import api.utils.db_utils as db_utils
i=1
for file in os.listdir("docs"):
    if file.endswith(".md"):
        file_path = os.path.join("docs", file)
        # file_id = db_utils.insert_document_record(file)
        file_id = i
        i+=1
        print(f"Processing file: {file_path} - ID: {file_id}")
        chroma_utils.index_document_to_chroma(file_path, file_id)
