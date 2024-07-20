import openai
import mysql.connector

# Initialize your OpenAI API key
openai.api_key = 'your openai key'

total_tokens_used = 0

def generate_response(topics, tokens_to_use):
    global total_tokens_used
    
    batch_size = 1  # Adjust batch size based on token usage
    for i in range(0, len(topics), batch_size):
        batch = topics[i:i+batch_size]
        for topic in batch:
            # Check if adding more tokens will exceed the limit
            estimated_tokens = 1000  # Approximate tokens for the request
            if total_tokens_used + estimated_tokens > tokens_to_use:
                print(f"Skipping topic '{topic}' to avoid exceeding the token limit.")
                continue
            
            # Create the prompt
            template = ('As an experienced data scientist and technical writer, generate a creative and engaging blog within 300-350 words '
                        'for a blog about {topic}. Make sure it is attractive and captivating to readers. Structure the content with headings, '
                        'subheadings, and sub-points using h2 and h3 tags appropriately.')
            prompt = template.format(topic=topic)
            
            try:
                # Run the LLM model to get the response
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,  # Reduced max tokens
                    temperature=0.7
                )
                
                # Extract the response content and token count
                response_content = response['choices'][0]['message']['content'].strip()
                tokens_used = response['usage']['total_tokens']
                
                if total_tokens_used + tokens_used > tokens_to_use:
                    print(f"Skipping topic '{topic}' to avoid exceeding the token limit.")
                    continue
                
                total_tokens_used += tokens_used
                
                # Generate HTML from the response
                html_output = generate_html(response_content)
                print("HTML Output:\n", html_output)
                print("Tokens used for this completion:", tokens_used)
                print("Total tokens used:", total_tokens_used)
                
                # Store the HTML output in MySQL
                store_html_in_mysql(topic, html_output)
                
            except openai.error.OpenAIError as e:
                print(f"An error occurred with topic '{topic}': {e}")

def generate_html(text):
    html_output = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Blog Post</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f9f9f9;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 20px auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                color: #2c3e50;
            }
            h2 {
                font-size: 2em;
                margin: 20px 0 10px;
                color: #2980b9;
            }
            h3 {
                font-size: 1.5em;
                margin: 15px 0 5px;
                color: #34495e;
            }
            p {
                margin-bottom: 15px;
                line-height: 1.8;
            }
            ul {
                list-style: disc;
                margin-left: 20px;
            }
            ol {
                list-style: decimal;
                margin-left: 20px;
            }
            li {
                margin-bottom: 10px;
            }
            a {
                color: #2980b9;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .footer {
                margin-top: 20px;
                padding: 10px 0;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #555;
            }
        </style>
    </head>
    <body>
        <div class="container">
    '''
    
    # Split content into lines and format HTML
    lines = text.split('\n')
    in_list = False
    for line in lines:
        line = line.strip()
        if line.startswith('Title:'):
            html_output += f'<h1>{line.replace("Title:", "").strip()}</h1>\n'
        elif line.startswith('The Future Innovations:') or line.startswith('Introduction:') or line.startswith('Overview:'):
            html_output += f'<h2>{line.replace("The Future Innovations:", "").replace("Introduction:", "").replace("Overview:", "").strip()}</h2>\n'
        elif line.startswith('Challenges:') or line.startswith('Key Features:') or line.startswith('Applications:'):
            html_output += f'<h3>{line.replace("Challenges:", "").replace("Key Features:", "").replace("Applications:", "").strip()}</h3>\n'
        elif line.startswith('- '):
            if not in_list:
                html_output += '<ul>\n'
                in_list = True
            html_output += f'<li>{line[2:].strip()}</li>\n'
        elif line.startswith('1. ') or line.startswith('2. '):
            if not in_list:
                html_output += '<ol>\n'
                in_list = True
            html_output += f'<li>{line[3:].strip()}</li>\n'
        else:
            if in_list:
                html_output += '</ul>\n'  # Close the list if it was open
                in_list = False
            html_output += f'<p>{line}</p>\n'
    
    if in_list:
        html_output += '</ul>\n'  # Ensure the list is closed if still open
    
    html_output += '''
        <div class="footer">
            <p>&copy; 2024 Your Company. All rights reserved.</p>
        </div>
    </div>
    </body>
    </html>
    '''
    return html_output

def store_html_in_mysql(topic, html_output):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="topic"
        )
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            topic VARCHAR(255) NOT NULL,
            html_content TEXT NOT NULL
        )
        """)
        
        # Insert HTML content into the table
        sql = "INSERT INTO blog_posts (topic, html_content) VALUES (%s, %s)"
        val = (topic, html_output)
        cursor.execute(sql, val)
        conn.commit()
        
        print(f"Record inserted for topic: {topic}")
        
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Example usage with a list of topics
topics = [
   "best day in 2024"
]

generate_response(topics, tokens_to_use=1000)