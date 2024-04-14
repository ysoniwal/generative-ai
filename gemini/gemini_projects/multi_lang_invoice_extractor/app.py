# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro 1.5 model
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

def get_gemini_response(genai_act_prompt, image, prompt):
    """
    genai_act_prompt: What we want the genai agent to act like
    image: The image input from where we are extracting information
        image is byte data of the image converted from uploaded image
        image[0] is "mime_type": uploaded_file.type -> See function input_image_details
    prompt: What information we want from the image

    Returns:
        response for the image and prompt provided
    """
    response=model.generate_content([genai_act_prompt, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    """
    It takes the uploaded image file,
    converts the image file to bytes and returns
    """
    if uploaded_file is not None:

        # Read file into Bytes:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Multi language invoice extractor")
st.header("Multi language invoice extractor App")

# Upload file
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

# Image is initially null
image=""
if uploaded_file is not None:
    # If image is uploaded then Open it
    image = Image.open(uploaded_file)

    # Display the Image:
    st.image(image, caption="Uploaded Image", use_column_width=True)

prompt = st.text_input("Your question: ", key="prompt")

submit=st.button("Submit")

# What we want GenAI agent to act like
genai_act_prompt="""
You are an expert in understanding invoices. We will upload an image as invoices and 
you are expected to answer any question based on the uploaded invoice image. 
"""

# If submit is clicked
if submit:
    # Extract image byte information from the image
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(genai_act_prompt, image_data, prompt)
    
    st.subheader("The response is")
    st.write(response)