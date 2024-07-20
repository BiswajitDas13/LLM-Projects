import os
import mysql.connector
from mysql.connector import Error
from constant import openai_key, mysql_config
from langchain_openai import OpenAI
import streamlit as st

# Setting the OpenAI API key
os.environ["OPENAI_API_KEY"] = openai_key

# Streamlit app setup
st.title("Langchain Demo with OpenAI API and MySQL")

# Input field for the user to enter a topic
input_text = st.text_input("Enter the topic you want to generate content about")

# Initialize the OpenAI model
llm = OpenAI(temperature=0.8)

# Function to save content to MySQL
def save_to_mysql(input_text, generated_text):
    try:
        print("Connecting to the database...")
        conn = mysql.connector.connect(**mysql_config)
        if conn.is_connected():
            print("Successfully connected to the database")
        cursor = conn.cursor()
        query = "INSERT INTO generated_content (input_text, generated_text) VALUES (%s, %s)"
        cursor.execute(query, (input_text, generated_text))
        conn.commit()
        cursor.close()
        conn.close()
        print("Content saved to database successfully!")
        st.success("Content saved to database successfully!")
    except Error as e:
        print(f"Error: {e}")
        st.error(f"Error: {e}")

# Generate and display the response if input text is provided
if input_text:
    response = llm(input_text)
    st.write(response)
    # Save the generated content to MySQL
    save_to_mysql(input_text, response)



