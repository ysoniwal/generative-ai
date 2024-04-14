# Load enviroment variables
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Langchain API to Instantiate Google Gemini Embeddings and Chat model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# Gemini 
import google.generativeai as genai

# Langchain FAISS embeddings API
from langchain.vectorstores import FAISS

# Langchain QA chains and Question Answering
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Configure Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Read multiple PDF files and convert to text strings
def get_pdf_text(pdf_docs):
    """
    Input: List of PDF files
    Output: Extracted text string from all the PDF files
    """
    text=""
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf) # Get detail of all the PDF pages in form of list

        for page in pdf_reader.pages: # For all pages in a PDF
            text += page.extract_text() # Extract the text present in a page

    return text

# Convert string of texts into chunks. It will be used later to create embeddings 
def get_text_chunks(text):
    """
    Convert text string created from all PDFs to chunks 
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Create embeddings using chunks and store them locally
def get_vector_store(text_chunks):
    """
    Convert Text chunks to embeddings using Gemini Embeddings model.
    Then store vector embeddings locally
    """
    # models/text-embedding-004  -> Supports elastic embedding sizes under 768.
    # models/embedding-001 -> Optimized for creating embeddings for text of up to 2048 tokens.
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    # Store vectors with name faiss_index
    vector_store.save_local("faiss_index")

# For the Google Chat Model, create prompt and chain
# Inputs to the prompt template are context and question
def get_conversational_chain():
    """
    Create a prompt Template, invoke Gemini Model, create chain and return
    """

    # Create Prompt template
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    """
    # Invoke Google Gemini Model
    model=ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)

    # Create prompt Template
    prompt=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Create Chain
    chain=load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(query):
    # Initiate embeddings
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # We have already stored the embeddings locally, here we are just reading those
    new_db = FAISS.load_local("faiss_index", embeddings)

    # Do similarity search of the user question in the loaded embeddings
    # It will give similar embeddings to the question
    docs = new_db.similarity_search(query)

    # Get chain that we have created earlier
    chain = get_conversational_chain()

    # Getting response: Here context is the similar vectors.
    # Question is the question from USER
    response = chain(
        {"input_documents": docs, "question": query},
        return_only_outputs=True
    )

    print(response)
    st.write("Reply: ", response["output_text"])

def main():
    st.set_page_config(page_title="Ask Multiple PDFs")
    st.header("Chat with PDF using Gemini")

    user_question = st.text_input("Ask a Question from the PDF files")

    # If the user asks question, then get the response
    if user_question:
        user_input(user_question)

    # The first step before question answering is Uploading the PDF and creating embeddings
    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload you PDF files and click Submit & Process Button", accept_multiple_files=True)
                                    
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text=get_pdf_text(pdf_docs)
                text_chunks=get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done", icon="✅")
    
if __name__ == "__main__":
    main()

