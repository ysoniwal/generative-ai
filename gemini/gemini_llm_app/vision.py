# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

from PIL import Image

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

# Function to load gemini pro model and get responses
def get_gemini_reponse(input, image):
    if input != "":
        response=model.generate_content([input, image])
    else:
        response=model.generate_content(image)
    return response.text

st.set_page_config(page_title="Gemini PRO 1.5 image application")
st.header("Gemini Image Application")
input=st.text_input("Input prompt: ", key="input")

# Upload file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Process and display image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit=st.button("Tell me about the image")
if submit:
    response=get_gemini_reponse(input, image)
    st.header("The response is")
    st.write(response)
