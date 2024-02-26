import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

from langchain.memory import ConversationBufferMemory

import streamlit as st

st.title("Celebrity Search Application")


# Prompt Template
first_input_template = PromptTemplate(
    input_variables=['name'],
    template="Tell me about Celebrity {name}."
)

# Memory
person_memory=ConversationBufferMemory(input_key='name', memory_key='chat_history')

llm = OpenAI(temperature=0.8)

chain=LLMChain(llm=llm, prompt=first_input_template, verbose=True, output_key='person', memory=person_memory)

# Prompt Template
second_input_template = PromptTemplate(
    input_variables=['person'],
    template="When was {person} born?"
)

dob_memory=ConversationBufferMemory(input_key='person', memory_key='chat_history')

chain2=LLMChain(llm=llm, prompt=second_input_template, verbose=True, output_key='dob', memory=dob_memory)

third_input_template = PromptTemplate(
    input_variables=['dob'],
    template="Mention 5 major events happened around that {dob}."
)

description_memory=ConversationBufferMemory(input_key='dob', memory_key='description_history')

chain3=LLMChain(llm=llm, prompt=third_input_template, verbose=True, output_key='description', memory=description_memory)

parent_chain=SequentialChain(chains=[chain, chain2, chain3], 
                             input_variables=['name'],
                             output_variables=['person', 'dob', 'description'],
                             verbose=True)

input_text = st.text_input("Search the topic you want")

if input_text:
    st.write(parent_chain({'name': input_text}))
  #st.write(parent_chain.run(input_text))
    
    with st.expander('Person Name'):
        st.info(person_memory.buffer)

    with st.expander('DOB'):
        st.info(dob_memory.buffer)
    
    with st.expander('Events'):
        st.info(description_memory.buffer)
    