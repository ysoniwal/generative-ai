# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import PyPDF2 as pdf

import google.generativeai as genai

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load google pro 1.5 model endpoint
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

def get_gemini_response(input_prompt, text):
    response=model.generate_content([input_prompt, text])
    return response.text

def input_pdf_to_text(uploaded_file):
    """
    Input: uploaded pdf file
    Output: all the text data of the pdf file
    """
    # Read the uploaded file
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for i in range(len(reader.pages)):
        page=reader.pages[i]
        text += str(page.extract_text())
    return text

input_prompt="""
    Act Like a skilled or very experience ATS(Application Tracking System)
    with a deep understanding of tech field,software engineering,data science ,data analyst
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide 
    best assistance for improving thr resumes. Assign the percentage Matching based 
    on Jd and
    the missing keywords with high accuracy
    resume:{text}
    description:{jd}

    I want the response in one single string having the structure
    {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_to_text(uploaded_file)
        response=get_gemini_response(input_prompt, text)
        st.subheader(response)
