# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import PyPDF2 as pdf

from youtube_transcript_api import YouTubeTranscriptApi

import google.generativeai as genai

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load google pro 1.5 model endpoint
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

prompt = """
You are a youtube video summarizer. You will be taking a youtube video transcript.
Your job is to summarize the transcript. Your output should be following:
1. The title or topic of the video 
2. Short summary (less than 50 words)
3. Long summary (within 300 words)
4. What is the percentage of relevant content. For this you have to cosider the part of summary where actual topic of the video is being discussed. 
For eg, you can ignore parts where the video promotes some related product or request for like, share, susbscribe etc., or tells about related
videos or content. 
All of the above have be done in both English and Hindi
Here is the trasnsript text:
"""

def get_gemini_response(prompt, transcript_text):
    """
    Input:
        prompt: What we want gen AI agent to do?
        transcript_text: Youtube video converted to transcript
    """
    response=model.generate_content(prompt + transcript_text)
    return response.text

def extract_youtube_transcript_detail(youtube_video_url):
    """
    YouTubeTranscriptApi API gives response in following format (List of dictionary):
        [
        {
            'text': 'Hey there',
            'start': 7.58,
            'duration': 6.13
        },
        {
            'text': 'how are you',
            'start': 14.08,
            'duration': 7.58
        },
        # ...
        ]
    """

    try:
        video_id = youtube_video_url.split("=")[1]
        video_transcipt = YouTubeTranscriptApi.get_transcript(video_id)

        # Coalate all the text from the response
        transcript_text = ""
        for transcipt in video_transcipt:
            transcript_text += " " + transcipt["text"]
        
        return transcript_text
    
    except Exception as e:
        raise e
    
# Frontend part
st.title("YouTube video summarizer App")
youtube_link = st.text_input("Enter Youtube video link", key='input_video')

if st.button("Enter") and youtube_link:
    # Show thumbnail
    video_id = youtube_link.split("=")[1]
    image_link = f"http://img.youtube.com/vi/{video_id}/0.jpg"
    st.image(image_link, use_column_width=True)
    st.text("URL fetch successfull. Click on Get Video Summary to proceed..")

if st.button("Get Video Summary"):
    transcript_text = extract_youtube_transcript_detail(youtube_link)
    if transcript_text is not None:
        response=get_gemini_response(prompt, transcript_text)
        st.subheader("Video summary is")
        st.write(response)
