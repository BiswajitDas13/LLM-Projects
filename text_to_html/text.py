import openai

# Initialize your OpenAI API key
openai.api_key = 'your openai key'

total_tokens_used = 0

def generate_response(topics, tokens_to_use):
    global total_tokens_used
    
    for topic in topics:
        # Check if adding more tokens will exceed the limit
        if total_tokens_used >= tokens_to_use:
            print("Exceeded token usage limit.")
            return
        
        # Create the prompt
        template = ('As an experienced data scientist and technical writer, generate a creative and engaging blog within 300-350 words'
                    ' for a blog about {topic}. Make sure it is attractive and captivating to readers.')
        prompt = template.format(topic=topic)
        
        # Run the LLM model to get the response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Extract the response content
        response_content = response.choices[0].message["content"].strip()
        
        # Calculate tokens used for this completion
        tokens_used = len(response_content.split())
        
        # Check if the next response will exceed the token limit
        if total_tokens_used + tokens_used > tokens_to_use:
            print("Exceeded token usage limit.")
            return
        
        total_tokens_used += tokens_used
        
        # Generate HTML, CSS, and JavaScript from the response
        html_output, css_output, js_output = generate_web_content(response_content)
        print("HTML Output:\n", html_output)
        print("CSS Output:\n", css_output)
        print("JavaScript Output:\n", js_output)
        print("Tokens used for this completion:", tokens_used)
        print("Total tokens used:", total_tokens_used)

def generate_web_content(text):
    lines = text.split('\n\n')
    
    html_output = '<html>\n<head>\n<title>Blog Post</title>\n'
    css_output = '<style>\n/* Add your CSS here */\nbody { font-family: Arial, sans-serif; margin: 40px; }\nh1 { color: #333; }\nh2 { color: #555; }\np { line-height: 1.6; }\n</style>\n'
    js_output = '<script>\n// Add your JavaScript here\ndocument.addEventListener("DOMContentLoaded", function() { console.log("Document is ready."); });\n</script>\n'
    
    html_output += css_output
    html_output += '</head>\n<body>\n'
    
    for line in lines:
        if 'Title:' in line:
            html_output += f'<h1>{line.replace("Title:", "").strip()}</h1>\n'
        elif 'AI:' in line or 'The Future Innovations:' in line:
            html_output += f'<h2>{line.strip()}</h2>\n'
        else:
            html_output += f'<p>{line.strip()}</p>\n'
    
    html_output += js_output
    html_output += '</body>\n</html>'
    return html_output, css_output, js_output

# Example usage with a single topic
topics = [
    "Revolutionizing E-Commerce with AI: Future Innovations and Impact"
]

generate_response(topics, tokens_to_use=1000)