import streamlit as st
from utils.pdf_processing import process_pdf_pages
from utils.llm_interaction import ask_question

# Initialize session state variables to avoid reloading and reprocessing
if 'document_data' not in st.session_state:
    st.session_state.document_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'question_input' not in st.session_state:
    st.session_state.question_input = ""

# Function to handle user question and get the answer
def handle_question(prompt):
    if prompt:
        # Use the cached document data for the query
        answer = ask_question(st.session_state.document_data, prompt)
        # Add the question-answer pair to the chat history
        st.session_state.chat_history.append({"question": prompt, "answer": answer})

# Streamlit application title
st.title("docQuest")

# Sidebar for file upload and document information
with st.sidebar:
    st.subheader("docQuest")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload and manage files here", type=["pdf"])

    # Process the PDF if uploaded and either not processed or a new file is uploaded
    if uploaded_file:
        # Check if the uploaded file is new or different from the previously uploaded file
        if 'last_uploaded_file' not in st.session_state or st.session_state.last_uploaded_file != uploaded_file:
            st.session_state.last_uploaded_file = uploaded_file
            st.session_state.document_data = None  # Reset document data
            st.session_state.chat_history = []  # Reset chat history
            
        # Process the PDF if not already processed
        if st.session_state.document_data is None:
            with st.spinner('Processing PDF...'):
                st.session_state.document_data = process_pdf_pages(uploaded_file)
            st.success("PDF processed successfully! Let's explore your document.")

# Main page for chat interaction
if st.session_state.document_data:
    st.subheader("Let us know more about your document..")
    
    # Create a placeholder container for chat history
    chat_placeholder = st.empty()

    # Function to display chat history dynamically
    def display_chat():
        with chat_placeholder.container():
            if st.session_state.chat_history:
                st.subheader("Chats", divider="orange")
                for chat in st.session_state.chat_history:
                    # ChatGPT-like alignment: user input on the right, assistant response on the left                
                    user_chat = f"<div style='float: right; display: inline-block; margin: 5px; border-radius: 8px; padding: 10px; margin-left: 3vw;'> {chat['question']}</div>"
                    assistant_chat = f"<div style='float: left; display: inline-block; margin: 5px; border-radius: 8px; padding: 10px; margin-right: 3vw;'> {chat['answer']}</div>"                    
                    st.markdown(f"\n")
                    st.markdown(user_chat, unsafe_allow_html=True)
                    st.markdown(assistant_chat, unsafe_allow_html=True)
                    st.markdown("---")

    # Display the chat history
    display_chat()

    # Input for user questions using chat input
    prompt = st.chat_input("Let me know what you want to know about your document..", key="chat_input")
    
    # Check if the prompt has been updated
    if prompt:
        handle_question(prompt)  # Call the function to handle the question
        st.session_state.question_input = ""  # Clear the input field after sending
        display_chat()  # Re-display the chat after adding the new entry
