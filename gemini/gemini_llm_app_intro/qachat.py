# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

# Get Response for the question from the Gemini 1.5 Pro Model
def get_chat_reponse(question):
    response=chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title="Q&A Chatbot")
st.header("Gemini Pro 1.5 Q&A Chat Bot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key='input')
submit = st.button("Ask me anything")

if submit and input:
    response=get_chat_reponse(input)
    ## Add user query and response to session chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Gemini Pro", chunk.text))

st.subheader("The chat history is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")