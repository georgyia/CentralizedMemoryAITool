import streamlit as st
from datetime import datetime
import openai
import time

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class ChatInterface:
    def __init__(self, openai_api_key):
        self.model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)
        self.output_parser = StrOutputParser()
        self.setup_streamlit()

    def setup_streamlit(self):
        st.set_page_config(page_title="Chat")

        # Initialize or retrieve conversations
        if "conversations" not in st.session_state:
            st.session_state.conversations = {}

        if "current_conversation" not in st.session_state:
            self.manage_conversation()

        # Sidebar for conversation history
        st.sidebar.title("Conversation history")
        if st.sidebar.button("Start new conversation"):
            self.manage_conversation()

        # List conversations in the sidebar
        self.display_conversation_list()

        # Display chat messages for the current conversation
        if st.session_state.current_conversation:
            self.display_chat_messages()
            self.handle_user_input()

    def manage_conversation(self, conversation_id=None):
        # Create or switch conversation
        if conversation_id:
            st.session_state.current_conversation = conversation_id
        else:
            current_time = datetime.now().strftime("%y-%m-%d %H:%M:%S")
            st.session_state.current_conversation = current_time
            st.session_state.conversations[current_time] = [{"role": "assistant", "content": "Let's start the conversation."}]

    def display_conversation_list(self):
        conversation_keys = sorted(st.session_state.conversations.keys(), reverse=True)
        for key in conversation_keys:
            conversation_title = key
            first_user_message = next((msg["content"] for msg in st.session_state.conversations[key] if msg["role"] == "user"), None)
            if first_user_message:
                conversation_title += f" - {first_user_message[:30]}"
            if st.sidebar.button(conversation_title):
                self.manage_conversation(conversation_id=key)

    def display_chat_messages(self):
        for message in st.session_state.conversations[st.session_state.current_conversation]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    def handle_user_input(self):
        prompt = st.chat_input("Enter your message:")
        if prompt:
            chat_history = st.session_state.conversations[st.session_state.current_conversation]
            chat_history.append({"role": "user", "content": prompt})
            chat_history = self.invoke_single_chain(prompt, chat_history)
            st.session_state.conversations[st.session_state.current_conversation] = chat_history
            st.experimental_rerun()

    def invoke_single_chain(self, user_input, chat_history):
        # Generate an answer using the model
        try:
            response = self.model.invoke(user_input)  # Pass string directly
            answer = self.output_parser.parse(response)
        except openai.RateLimitError as e:
            delay = 5  # Delay in seconds before retrying
            print(f"Rate limit exceeded. Retrying in {delay} seconds...")
            time.sleep(delay)
            chat_history.append({"role": "assistant", "content": "Sorry, I'm experiencing high traffic. Please try again later."})
            return chat_history

        # Save the content of the answer in the chat history
        chat_history.append({"role": "assistant", "content": answer.content})

        return chat_history

if __name__ == "__main__":
    openai_api_key = "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"
    chat_interface = ChatInterface(openai_api_key)
