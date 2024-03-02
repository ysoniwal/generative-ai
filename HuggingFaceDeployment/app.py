from langchain_openai import OpenAI, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import streamlit as st
import os

#load_dotenv()

llm=ChatOpenAI(temperature=0.6)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="You are a comedian AI assistant")
    ]

def get_chat_model_reponse(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer = llm(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))

    return answer.content


st.set_page_config(page_title="Q & A Demo")
st.header("Let's Chat")

input=st.text_input("Input: ", key="input")
response=get_chat_model_reponse(input)

submit=st.button("Ask me anything")

if submit:
    st.subheader("Reponse is")
    st.write(response)