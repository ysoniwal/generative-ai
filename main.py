import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain.llms import OpenAI

import streamlit as st

st.title("Langchain Demo with OpenAI API")
input_text = st.text_input("Search the topic you want")

llm = OpenAI(temperature=0.8)

if input_text:
  st.write(llm(input_text))