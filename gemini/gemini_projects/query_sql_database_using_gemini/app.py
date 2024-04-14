import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import sqlite3

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load gemini Pro 1.5 Model
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

# Function to genrate response from the natural language question
# Expected output here is a SQL query
def get_gemini_response(prompt, question):
    """
    Inputs:
        prompt: How we want our gen AI agent to act like
        question: Our Natural Language question to the gen ai agent
    Output:
        response using the prompt and question
    """
    response=model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve data from the SQL database
def run_sql_query(sql_query, db):
    """
    Inputs:
        sql_query: String format SQL query to execute on DB
        db: DataBase where we have to make connection
    Output:
        Output of SQL query
    """
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql_query)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows

prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are there in the table?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
    \nExample 2 - All the information of students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

st.set_page_config(page_title="Natural Language to SQL query")
st.header("Natural Language to SQL query APP")

input = st.text_input("Query in Natural Language: ", key="input")
submit = st.button("Go!")

if submit:
    # Convert to query and display
    sql_query=get_gemini_response(prompt, input)
    st.subheader("Corresponding Query is:")
    st.write(sql_query)

    # Query the response in SQLite table
    rows=run_sql_query(sql_query, "student.db")
    st.subheader("Query Result is:")
    for row in rows:
        st.write(row)



