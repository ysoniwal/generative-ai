import os
from dotenv import load_dotenv
load_dotenv()

from PIL import Image

import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

def get_gemini_response(input_prompt, image):
    response=model.generate_content([input_prompt, image])
    return response.text

st.set_page_config(page_title="Food Nutrition Info App")
st.header("Food Nutrition Info App")

# Display a file uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

input_prompt = """
You are an expert dietician. You will be given an image of food items or a meal. 
If it is not a food image, then you have to tell the user to upload the food related
images only. 
If the uploaded image is of food, then you have to understand all the items present in the image,
look at the quantity and you have to output the following:
1. What cuisine it belongs to
2. All the items present in the image 
3. Thier approximate calaries information and total calaries
4. Recommend whether they are good for health or not?
"""

if uploaded_file is not None:
    # Read the image file
    image = Image.open(uploaded_file)
    
    # Display the image
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Add a submit button
    if st.button("Submit"):
        # Perform some action when the button is clicked

        response=get_gemini_response(input_prompt, image)
        st.subheader("Gemini Response:")
        st.write(response)
