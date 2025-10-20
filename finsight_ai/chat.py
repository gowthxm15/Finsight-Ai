import streamlit as st
from utils.file_handler import load_excel_file
from utils.llm import ask_llm


def launch_chat():
    st.title("💬 Chat Assistant")
    
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("📁 Please upload your Excel data first from the 'Upload Data' section.")
        return

    df = st.session_state.df
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask something about your finances...", key="chat_input")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your data..."):
                try:
                    response = ask_llm(user_input, df)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't process that."})
    
