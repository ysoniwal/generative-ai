from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

from typing_extensions import Concatenate

from langchain.chains.question_answering import load_qa_chain

from dotenv import load_dotenv

load_dotenv()

def read_pdf(filename):
    pdf_reader = PdfReader(filename)

    raw_text = ''
    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            raw_text += content
    return raw_text

def split_text(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 800,
        chunk_overlap = 200,
        length_function = len
    )
    texts = text_splitter.split_text(raw_text)
    return texts


if __name__ == '__main__':
    raw_text = read_pdf("budget_speech.pdf")
    texts = split_text(raw_text)

    embeddings = OpenAIEmbeddings()

    document_search = FAISS.from_texts(texts, embeddings)

    chain = load_qa_chain(llm=OpenAI(), chain_type='stuff')

    query = "How much is sports, agriculture and defence budget this year?"
    docs = document_search.similarity_search(query)
    print(chain.run(input_documents=docs, question=query))


    