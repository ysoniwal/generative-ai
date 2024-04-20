import os
from youtube_transcript_api import YouTubeTranscriptApi
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PC
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

import streamlit as st

def display_video_thumbnail(youtube_video_url):
    video_id = youtube_video_url.split("=")[1]
    image_link = f"http://img.youtube.com/vi/{video_id}/0.jpg"
    st.image(image_link, use_column_width=True)
    st.write("Transcript Fetched. Generating Summary...")

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

def get_pinecone_index(transcript_text, max_chars, chunk_overlap):
    # Vector Store
    # Create chunks from text for converting to embeddings
    ts = RecursiveCharacterTextSplitter(chunk_size=max_chars, chunk_overlap=chunk_overlap)
    chunks = ts.split_text(transcript_text)

    # Create embeddings using OpenAIEmbeddings model
    # This model has default embedding size (1536) and doesn't support changing it
    embeddings_model = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])

    # Store these embeddings in vector databases. Index name we have created is youtubetranscribevector
    pinecone_index = upsert_to_pinecone_index("youtubetranscribevector", chunks, embeddings_model)

    return pinecone_index


def upsert_to_pinecone_index(index_name, chunks, embeddings_model):
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index = pc.Index(index_name)
    # Delete all existing vectors in the index
    try:
        index.delete(delete_all=True)
    except: # If the index in empty for the first time, then no namespace will be present (default namespace = default)
        pass

    # Upsert all the chunks, conveted to embeddings to the index we have created in pinecone
    index=PC.from_texts(chunks, embeddings_model, index_name=index_name)
    return index

def preprocess_transcipt(youtube_link, llm_model, max_chars, chunk_overlap):
    pinecone_index = None

    # Display thumbnail
    display_video_thumbnail(youtube_link)

    # Extract transctipt of the youtube video
    transcript_text = extract_youtube_transcript_detail(youtube_link)
    
    # Prompt for generating summary
    prompt_summary = """
        You are a youtube video summarizer. You will be taking a youtube video transcript.
        Your job is to summarize the transcript. Your output should be following:
        1. The title or topic of the video 
        2. Short summary (less than 50 words)
        3. Long summary (within 300 words)
        4. What is the percentage of relevant content. For this you have to cosider the part of summary where actual topic of the video is being discussed. 
        For eg, you can ignore parts where the video promotes some related product or request for like, share, susbscribe etc., or tells about related
        videos or content. 
        You have to give response in same language as that of the primary language of this video.
        Here is the trasnsript text:
        """
        
    if transcript_text is not None:
        # Display Video Summary
        video_summary=llm_model.generate_content(prompt_summary + transcript_text)
        video_summary=video_summary.text
        st.subheader("Video summary is")
        st.write(video_summary)

        pinecone_index = get_pinecone_index(transcript_text, max_chars, chunk_overlap)
        
        # st.write("Vector Store created !!!")
        st.success("Summary Generated!!", icon="✅")

        return pinecone_index
    
def get_query_response(llm_model, user_query, maching_documents):
    prompt = """
    You will be given some context and you will be asked a question. You have to provide answer from the specified context only.
    If the answer is not present in the context, don't give wrong answer. You can mention that you need more information.
    User question is : 
    """

    response=llm_model.generate_content(prompt + user_query + str(maching_documents))
    return response.text
