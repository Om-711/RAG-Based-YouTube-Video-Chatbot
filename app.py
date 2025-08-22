import streamlit as st
from function_chatbot import url_2_id, indexing, retriever_chain
import os

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyCRBh9QM7vdjEOxyB9x5OjQPF0oXeZaHyM"

st.set_page_config(page_title="YouTube ChatBot ❤️", layout="wide")
st.title("YouTube ChatBot ❤️")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "video_id" not in st.session_state:
    st.session_state.video_id = None

user_text_url = st.text_input("Enter YouTube Link")

if st.button("Load Video"):
    try:
        video_id = url_2_id(user_text_url)
        st.session_state.vector_store = indexing(video_id)
        st.session_state.messages = []   # reset old chat
        st.session_state.video_id = video_id
        st.success("Video loaded! Now ask your questions below.")
    except Exception as e:
        st.error(f"Error: {e}")


if st.session_state.vector_store:
    col1, col2 = st.columns([1, 2])  # Left = 1 part, Right = 2 parts

    # Left column -> video 
    with col1:
        if st.session_state.video_id:
            video_url = f"https://www.youtube.com/watch?v={st.session_state.video_id}"
            st.video(video_url) 
            # thumbnail only:
            # st.image(f"https://img.youtube.com/vi/{st.session_state.video_id}/0.jpg", use_container_width=True)

    # Right column → Chat
    with col2:
        user_input = st.chat_input("Ask something about the video...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.spinner("Thinking..."):
                try:
                    response = retriever_chain(st.session_state.vector_store, user_input)
                except Exception as e:
                    response = {"text": f"Error: {e}"}

                st.session_state.messages.append({"role": "assistant", "content": response['text']})

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
