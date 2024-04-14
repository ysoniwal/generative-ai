# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

# Function to load gemini pro model and get responses
def get_gemini_reponse(question):
    response=model.generate_content(question)
    return response.text

# Initial streamlit app
st.set_page_config(page_title="Gemini Q&A App")
st.header("Gemini Pro 1.5 application")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# When submit is clicked
if submit:
    response=get_gemini_reponse(input)
    st.subheader("The response is")
    st.write(response)

 

