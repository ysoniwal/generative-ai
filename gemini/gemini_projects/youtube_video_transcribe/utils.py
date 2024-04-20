import os
from youtube_transcript_api import YouTubeTranscriptApi
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PC

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
 
def get_pinecone_index(index_name, chunks, embeddings_model):
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

def get_query_response(llm_model, user_query, maching_documents):
    prompt = """
    You will be given some context and you will be asked a question. You have to provide answer from the specified context only.
    If the answer is not present in the context, don't give wrong answer. You can mention that you need more information.
    User question is : 
    """

    response=llm_model.generate_content(prompt + user_query + str(maching_documents))
    return response.text

    