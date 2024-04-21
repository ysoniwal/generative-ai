# This file creates SQLite database (student DB and insert some records)

# Comes by default with python installation
import sqlite3

# Connect to sqlite3 and create DataBase
connection=sqlite3.connect("student.db")

# Create a cursor object to insert record, create table, retrieve results
cursor=connection.cursor()

# Create the table
table_info="""
    CREATE TABLE STUDENT(
    name VARCHAR(25),
    class VARCHAR(25),
    section VARCHAR(25),
    marks INT
);
"""
cursor.execute(table_info)

# Add records
cursor.execute("""INSERT INTO student values('Yogesh', 'Data Science', 'A', 80)""")
cursor.execute("""INSERT INTO student values('Jyoti', 'Data Science', 'B', 100)""")
cursor.execute("""INSERT INTO student values('Arya', 'Machine Learning Engineer', 'A', 90)""")
cursor.execute("""INSERT INTO student values('Mohit', 'Software Engineer', 'A', 90)""")
cursor.execute("""INSERT INTO student values('Vikash', 'Data Analyst', 'A', 70)""")
cursor.execute("""INSERT INTO student values('Suresh', 'Machine Learning Engineer', 'A', 100)""")
cursor.execute("""INSERT INTO student values('Ram', 'Software Engineer', 'B', 20)""")
cursor.execute("""INSERT INTO student values('Parthi', 'Data Analyst', 'A', 0)""")
cursor.execute("""INSERT INTO student values('Suhash', 'Data Science', 'A', -20)""")

# Display all the records
print("Inserted records are")

data=cursor.execute("""SELECT * FROM student""")

for row in data:
    print(row)

# Close the connection
connection.commit()
connection.close()
