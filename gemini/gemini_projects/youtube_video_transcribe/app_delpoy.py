# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Set maximum characters per chunk for processing
max_chars = 1000
chunk_overlap = 100

import streamlit as st

from utils import extract_youtube_transcript_detail
from utils import get_pinecone_index
from utils import get_query_response

import google.generativeai as genai

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Configure Generative AI with Google API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load google pro 1.5 model endpoint
llm_model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

# # Load gemini embeddings
# embeddings_model = genai.GenerativeModel('models/embedding-001')
embeddings_model = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])

def user_question_response(youtube_link, user_question):
    # Step 1. From the input YouTube url, transcribe to text
    # Frontend part

    

            user_query = st.text_input("Ask anything about the video", key='user_query')
            if st.button("Enter") and user_query:

                # Step 2. Create chunks from text for converting to chunks
                ts = RecursiveCharacterTextSplitter(chunk_size=max_chars, chunk_overlap=chunk_overlap)
                chunks = ts.split_text(transcript_text)

                # Step 3. Create embeddings using OpenAIEmbeddings model
                # This model has default embedding size (1536) and doesn't support changing it
                embeddings_model = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])

                # Step 4. Store these embeddings in vector databases. Index name we have created is youtubetranscribevector
                index = get_pinecone_index("youtubetranscribevector", chunks, embeddings_model)

                # Step 5. For the specified query, search similar results
                #user_query = "What is unemployment rate in Indian currently"
                user_query = user_question
                maching_documents=index.similarity_search(user_query, k=5)

                # Step 6. Answer user query from the document
                response = get_query_response(llm_model, user_query, maching_documents)

                st.write(response)

def main():
    st.set_page_config(page_title="Ask questions from YouTube video")
    
    transcript_text = ""
    video_summary = ""
    youtube_link = ""
    selected_option = None
    
    # The first step before question answering is Uploading the PDF and creating embeddings
    with st.sidebar:
        st.title("YouTube video Q&A App")
        youtube_link = st.text_input("Enter Youtube video link", key='input_video')

        if st.button("Enter") and youtube_link:
            # Show thumbnail
            video_id = youtube_link.split("=")[1]
            image_link = f"http://img.youtube.com/vi/{video_id}/0.jpg"
            st.image(image_link, use_column_width=True)
            st.text("URL fetch successfull. Click on Get Video Summary to proceed..")
            st.success("Done", icon="✅")

            selected_option = st.selectbox("Choose an option:", ["Video Summary", "Question from video"])

    if selected_option:
        #if st.button("Get Video Summary"):
            transcript_text = extract_youtube_transcript_detail(youtube_link)
            prompt_summary = """
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
                
            if transcript_text is not None:
                video_summary=llm_model.generate_content(prompt_summary + transcript_text)
                video_summary=video_summary.text
                #st.subheader("Video summary is")
                #st.write(response.text)

            if selected_option == "Video Summary":
                st.write(video_summary)
            elif selected_option == "Question from video":
                st.write("Test")
    # print(youtube_link)
    # # If the user asks question, then get the response
    # st.header("Ask a question after uploading YouTube video URL")
    # user_question = st.text_input("Ask a Question from video")
    # if user_question:
    #     user_question_response(youtube_link, user_question)
    #     pass
    
if __name__ == "__main__":
    main()