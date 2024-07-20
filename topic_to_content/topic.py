import openai

# Initialize total_tokens_used outside the function to track total usage
total_tokens_used = 0

def generate_response(topics, tokens_to_use):
    global total_tokens_used
    
    # Initialize OpenAI API key
    openai.api_key = 'your openai key'
    
    for topic in topics:
        # Check if adding more tokens will exceed the limit
        if total_tokens_used >= tokens_to_use:
            print("Exceeded token usage limit.")
            return
        
        # Create the prompt template
        template = ('As an experienced data scientist and technical writer, generate a creative and engaging blog within 300-350 words'
                    ' for a blog about {topic}. Make sure it is attractive and captivating to readers.')
        prompt = template.format(topic=topic)
        
        # Run the LLM model to get the response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7  # Increased temperature for more creativity
        )
        
        # Get the response content
        response_content = response['choices'][0]['message']['content']
        
        # Calculate tokens used for this completion
        tokens_used = len(response_content.split())
        
        # Check if the next response will exceed the token limit
        if total_tokens_used + tokens_used > tokens_to_use:
            print("Exceeded token usage limit.")
            return
        
        total_tokens_used += tokens_used
        
        # Print out the response with merged Introduction section
        print(f"Blog outline for topic '{topic}':")
        outline = response_content.replace('\n', ' ').replace('\r', ' ')
        outline = outline.replace('. ', '.\n\n')  # Add double newline after each sentence
        print(outline)
        print("Tokens used for this completion:", tokens_used)
        print("Total tokens used:", total_tokens_used)
        print("\n")  # Add newline for clarity

# Example usage with a single topic
topics = [
    "how AI will help digital marketing"
]

generate_response(topics, tokens_to_use=1000)

