import openai

# Set your OpenAI API key
openai.api_key = 'your apikey'


def get_related_topics(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,  # Adjust token length as needed
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Single text prompt
prompt = "List related topics to Natural Language Processing (NLP)"

# Get related topics
related_topics = get_related_topics(prompt)
print("Related Topics to NLP:")
print(related_topics)
