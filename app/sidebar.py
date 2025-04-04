import streamlit as st
import requests
import datetime
# def sidebar():    
#     st.sidebar.header("Previous History")
#     # Initialize document list if not present
#     if "documents" not in st.session_state:
#         st.session_state.documents = requests.post("http://localhost:3100/api/v1/chat", json=data, stream=True)

#     documents = st.session_state.documents
#     if documents:
#         for doc in documents:
#             st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})")
        
#         # Delete Document
#         selected_file_id = st.sidebar.selectbox("Select a document to delete", options=[doc['id'] for doc in documents], format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))
#         if st.sidebar.button("Delete Selected Document"):
#             with st.spinner("Deleting..."):
#                 delete_response = delete_document(selected_file_id)
#                 if delete_response:
#                     st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
#                     st.session_state.documents = list_documents()  # Refresh the list after deletion
#                 else:
#                     st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")

def fetch_user_sessions(username:str):
    response = requests.get(f"http://localhost:3100/api/v1/chat/usersessions/{username}")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def fetch_session_messages(session_id):
    response = requests.get(f"http://localhost:3100/api/v1/chat/sessionhistory/{session_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def sidebar(username:str = None):
    if st.sidebar.button("Logout"):
        del st.session_state.token
        del st.session_state.github_user
        del st.session_state.messages
        st.session_state["logout_triggered"] = True
        st.rerun()
    st.sidebar.header("Your Chat History")
    chat_history = fetch_user_sessions(username) if username else []
        
    if chat_history:
        session_ids = [session['session_id'] for session in chat_history['sessions']]
        selected_session_id = st.sidebar.selectbox("",
            options=session_ids,
            format_func=lambda x: next(session['message'] for session in chat_history['sessions'] if session['session_id'] == x)
        )
        
        if selected_session_id and st.sidebar.button("Load Selected Session"):
            session_messages = fetch_session_messages(selected_session_id)
            if session_messages:
                last_active = next(session['last_active'] for session in chat_history['sessions'] if session['session_id'] == selected_session_id)
                last_active_dt = datetime.datetime.fromisoformat(last_active)
                formatted_last_active = last_active_dt.strftime("%B %d, %Y %I:%M %p")
                st.write(f"Chat Session ID: {selected_session_id} - Last Active: {formatted_last_active}")
                st.session_state.messages = []
                for message in session_messages['messages']:
                    # st.write(f"{message['role']}: {message['content']}")
                    if message['role'] == "user":
                        st.session_state.messages.append({
                            "user": username, 
                            "role": "user", 
                            "content": message['content'],
                            "avatar": st.session_state.github_user['avatar_url']
                        })
                    else:
                        st.session_state.messages.append({
                            "user": "bot", 
                            "avatar":"https://avatars.githubusercontent.com/u/28813424?s=48&v=4", 
                            "role": "assistant", 
                            "content": message['content']
                        })
            else:
                st.write("Failed to load chat session.")
    else:
        st.sidebar.write("No previous chat history found.")

st.sidebar.title("Loki's chatbot")

