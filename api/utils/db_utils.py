import psycopg2
import os

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "genai"),
    "user": "postgres",  # Default PostgreSQL user
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": "5432",  # Default PostgreSQL port
}

chat_table = "ai.tbl_chat_history"
document_table = "ai.tbl_documents"

def connect_db():
    """Establish connection to PostgreSQL."""
    return psycopg2.connect(**DB_PARAMS)

def create_table():
    """Create a table if it doesn't exist."""
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INT NOT NULL
                )
            """)
            conn.commit()

def insert_chat_history(username:str, rolename:str, session_id:str, message:str):
    """Insert data into the users table."""
    get_parent_id = f"""
        SELECT id FROM {chat_table} WHERE session_id = '{session_id}' AND username = '{username}' ORDER BY id DESC LIMIT 1
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(get_parent_id)
            parent_id = cur.fetchone()
            if parent_id is None:
                # First message, insert without parent_id
                cur.execute(f"""
                    INSERT INTO {chat_table} (username, rolename, session_id, message)
                    VALUES (%s, %s, %s, %s)
                """, (username, rolename, session_id, message))
                
            else:
                cur.execute(f"""
                    INSERT INTO {chat_table} (session_id, username, rolename, message, parent_message_id)
                    VALUES (%s, %s, %s, %s, %s)
                """,(session_id, username, rolename, message, parent_id[0]))
            cur.execute(get_parent_id)
            conn.commit()

def get_chat_history(username:str, session_id:str):
    """Retrieve chat history from the users table."""
    messages = []
    with connect_db() as conn:
        with conn.cursor() as cur:
            query = f"""
                SELECT rolename, message
                FROM {chat_table}
                WHERE session_id = '{session_id}' AND username = '{username}'
                ORDER BY id
            """
            cur.execute(query)
            for row in cur.fetchall():
                messages.append({"role": row[0], "content": row[1]})
    return messages
            
def insert_document_record(filename:str):
    """Insert a record for the uploaded document."""
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {document_table} (filename) VALUES ('{filename}') RETURNING id
            """)
            document_id = cur.fetchone()[0]
            conn.commit()
            return document_id

def fetch_data(query):
    """Retrieve all records from the users table."""
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
if __name__ == "__main__":
    create_table()
    # Example usage
    insert_chat_history("user", "assistant", "session_123", "Hello how can I help you")
