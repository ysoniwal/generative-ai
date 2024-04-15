# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image

import google.generativeai as genai

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load google pro 1.5 model endpoint
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

def get_gemini_response(prompt, pdf_content, input_text):
    """
    Input:
        prompt: How we want Gen AI agent to Act like
        pdf_content: PDF to image converted content
        input_text: What we want to know from the PDF
    Return:
        Gemini Response
    """
    response=model.generate_content([prompt, pdf_content[0], input_text])
    return response.text

def input_pdf_processing(uploaded_file):
    """
    Input: uploaded image file
    Output: 
        Convert uploaded image to byte, save it as JPEG

    """
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes: 
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr=img_byte_arr.get_value()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.base64encode(img_byte_arr).decode()  
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")
    
st.set_page_config(page_title="Resume ATS APP")
st.header("ATS Tracking System")

input_text=st.text_area("Job Description: ", key="input")

uploaded_file=st.file_uploader("Upload your Resume in PDF format", type=["pdf"])

if uploaded_file is not None:
    st.write("File Uploaded Successfully")

submit1 = st.button("Tell me about the resume")
submit2 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced HR with experience in technology such as data science, full stack development,
 devops, web development, big data engineering, data analytics.
 Your task is to review the provided resume against the job description for these profiles. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, full stack development,
 devops, web development, big data engineering, data analytic and deep ATS functionality, your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. 
First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_processing(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the Resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_processing(uploaded_file)
        response=get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the Resume")
