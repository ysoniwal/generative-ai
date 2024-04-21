# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Set maximum characters per chunk for processing
max_chars = 1000
chunk_overlap = 100

import streamlit as st

from utils import preprocess_transcipt
from utils import get_conversational_chain

import google.generativeai as genai

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load google pro 1.5 model endpoint
llm_model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

def main():
    st.set_page_config(page_title="YouTube video Q&A App")
    
    st.title("YouTube video Q&A App")
    youtube_link = st.text_input("Enter Youtube video link", key='input_video')

    # This is query entered by user. Initializing with empty
    user_query = st.empty()
    # Whether pre processing is complete or not
    processing_complete = False

    button1 = st.button('Submit')
    # In streamlit state of a button is True only when it is clicked
    # As soon as any other action is performed on the page, the state
    # again becomes False. Here we are storing state of the first button
    if st.session_state.get('button') != True:
        st.session_state['button'] = button1

    if st.session_state['button'] and youtube_link:
        pinecone_index = preprocess_transcipt(youtube_link, llm_model, max_chars, chunk_overlap)
        processing_complete = True
    
        user_query = ""
        if processing_complete:
            #if vector_store:
            user_query = st.text_input("Ask anything about the video", key='user_query')
            #st.write(user_query)

        if st.button("Ask") and user_query:

            # For the specified query, search similar results
            matching_documents = pinecone_index.similarity_search(user_query, k=5)

            # Get Conversation Chain from langchain Google Chat API
            chain = get_conversational_chain()

            response = chain(
                {"input_documents": matching_documents, "question": user_query},
                return_only_outputs=True
            )

            st.write(response)
        
if __name__ == "__main__":
    main()