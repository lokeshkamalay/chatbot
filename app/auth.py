import streamlit as st
from streamlit_oauth import OAuth2Component
import os
import requests
from dotenv import load_dotenv
import ollama
import json
import time
load_dotenv()

# Set environment variables
AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
REVOKE_TOKEN_URL = "https://api.github.com/applications/Ov23linJ4cYBvaWeEyw2/token"
CLIENT_ID = "Ov23linJ4cYBvaWeEyw2"
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")  # Use .env for secrets
REDIRECT_URI = "http://localhost:8501/component/streamlit_oauth.authorize_button/index.html"
SCOPE = "user"
ALLOWED_ORG = "suvofficial"

if "token" not in st.session_state:
    st.session_state.setdefault("token", None)
if "github_user" not in st.session_state:
    st.session_state.setdefault("github_user", None)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = ""

# Create OAuth2Component instance
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, None, REVOKE_TOKEN_URL)
# Sidebar
st.sidebar.title("Loki's chatbot")
st.sidebar.header("Useful Links")
st.sidebar.markdown("[Home](http://localhost:8501)")
st.sidebar.markdown("[About](http://localhost:8501/about)")
st.sidebar.markdown("[Contact](http://localhost:8501/contact)")
# st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())  # Clear session state on Logout button

st.title("Loki's chatbot")
st.logo(
    image="https://s202.q4cdn.com/986123435/files/doc_downloads/logos/american-airlines/THUMB-aa_aa__ahz_4cp_grd_pos-(1).png",
    size="large",  # Options: "small", "medium", "large"
    link="https://www.aa.com"
)
def get_github_user(token):
    headers = {"Authorization": f"Bearer {token.get('access_token')}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def validate_user(token):
    headers = {"Authorization": f"Bearer {token.get('access_token')}"}
    response = requests.get("https://api.github.com/user/orgs", headers=headers)
    if response.status_code == 200:
        orgs = [org['login'] for org in response.json()]
        return ALLOWED_ORG in orgs
    return False

# def generate_response():
#     response = ollama.chat(model='llama3.2', stream=True, messages=st.session_state.messages)
#     for partial_resp in response:
#         token = partial_resp["message"]["content"]
#         st.session_state["full_message"] += token
#         yield token

if not st.session_state.token:
    # Show the authorize button
    result = oauth2.authorize_button("Authorize with GitHub", REDIRECT_URI, SCOPE)
    if result and "token" in result:
        # Save token in session state
        st.session_state.token = result["token"]
        # Get GitHub user info
        user_info = get_github_user(st.session_state.token)
        if user_info:
            st.success(f"Welcome, {user_info['login']}! 🎉")
            if validate_user(st.session_state.token):
                st.session_state.github_user = user_info
                st.session_state.messages.append({
                    "user": "bot", 
                    "avatar":"https://avatars.githubusercontent.com/u/28813424?s=48&v=4", 
                    "role": "assistant", 
                    "content": f"Hello {user_info['name']}! How can I assist you today? for best results please include the tool/technology name you need help with like github cloudsmith artifactory"
                })
            else:
                st.markdown(f"<h1 style='color: red;'>🚫 User {user_info['login']} is not authorized to access this bot<br/><br/>Contact DTE for help</h1>", unsafe_allow_html=True)
                st.stop()
        else:
            st.error("Failed to fetch GitHub user info.")
        st.rerun()

if "logout_triggered" in st.session_state:
    st.empty()  # Clears everything on the page
    st.header("Thank you for using Loki's chatbot!")
    st.markdown("Hope was able to help you! If you have any feedback, please reach out to us below,")
    st.markdown("[Slack](http://localhost:8501)")
    del st.session_state.logout_triggered
    # st.rerun()

if st.session_state.github_user is not None:
    st.subheader(f"Welcome, {st.session_state.github_user['login']}! 🎉")
    if st.sidebar.button("Logout"):
        del st.session_state.token
        del st.session_state.github_user
        del st.session_state.messages
        st.session_state["logout_triggered"] = True
        st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["user"], avatar=message.get("avatar")):
            st.markdown(message["content"])
    if prompt := st.chat_input("Type your question here"):
        st.session_state["last_active"] = time.time() # Refresh session activity
        chunks = prompt
        st.session_state.messages.append({
                "user": st.session_state.github_user['login'], 
                "role": "user", 
                "content": prompt,
                "avatar": st.session_state.github_user['avatar_url']
            })
        with st.chat_message(
                st.session_state.github_user['login'], 
                avatar=st.session_state.github_user['avatar_url']):
            st.markdown(prompt)
        st.session_state["full_message"] = ""
        data = {
            "username": st.session_state.github_user['login'],
            # "messages": st.session_state.messages,
            "messages": prompt,
            "model": "llama3.2",
            "session_id": st.session_state.session_id
        }
        with st.spinner("Generating response..."):
            response_placeholder = st.empty()
            response = requests.post("http://localhost:3100/api/v1/chat", json=data, stream=True)
            response_text = ""
            
            if st.session_state.session_id == "":
                st.session_state.session_id = response.headers.get("X-Session-ID")

            with st.chat_message("bot", avatar="https://avatars.githubusercontent.com/u/28813424?s=48&v=4"):
                response_container = st.empty()
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        response_text += chunk.decode()
                        response_container.markdown(response_text)
            st.session_state.messages.append({
                "user": "bot", 
                "avatar":"https://avatars.githubusercontent.com/u/28813424?s=48&v=4", 
                "role": "assistant", 
                "content": response_text
            })
        # with st.spinner("Generating response..."):
        #     response = requests.post("http://localhost:3100/api/v1/chat", json=data)
        #     with st.chat_message("bot", avatar="https://avatars.githubusercontent.com/u/28813424?s=48&v=4"):
        #         st.markdown(response.json().get("answer"))
        #     st.session_state.messages.append({
        #         "user": "bot", 
        #         "avatar":"https://avatars.githubusercontent.com/u/28813424?s=48&v=4", 
        #         "role": "assistant", 
        #         "content": response.json().get("answer")
        #     })
