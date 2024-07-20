# flask_app.py
from flask import Flask, request, jsonify
import openai
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# OpenAI API configuration
openai.api_key = 'your openai key'

# MySQL configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'Ai_data'
}

def create_database_and_table():
    try:
        cnx = mysql.connector.connect(
            user=db_config['user'], 
            password=db_config['password'], 
            host=db_config['host']
        )
        cursor = cnx.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Ai_data")
        cursor.execute("USE Ai_data")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS topics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            topic VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        cursor.close()
        cnx.close()
    except Error as e:
        print(f"Error: {e}")

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    topic = data.get('topic')
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    try:
        # Generate content using OpenAI
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Write a detailed article on the topic: {topic}"}
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        content = response.choices[0].message['content'].strip()

        # Ensure the database and table exist
        create_database_and_table()

        # Connect to MySQL
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Insert the topic and content into the database
        insert_query = "INSERT INTO topics (topic, content) VALUES (%s, %s)"
        cursor.execute(insert_query, (topic, content))
        cnx.commit()

        # Close the connection
        cursor.close()
        cnx.close()

        return jsonify({"topic": topic, "content": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
