import openai
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import re

# Download NLTK resources if not already downloaded
nltk.download('punkt')

# Set your OpenAI API key
openai.api_key = 'your openai key'

def generate_initial_content(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use the latest model for best results
        messages=[
            {"role": "system", "content": "You are a knowledgeable and helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,  # Increase tokens for more content
        temperature=0.9  # Higher temperature for creativity
    )
    return response.choices[0].message['content'].strip()

def humanize_text(text):
    sentences = sent_tokenize(text)
    humanized_sentences = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        
        # Introduce subtle errors or informal language
        if random.random() < 0.4:  # 40% chance to modify
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx][::-1]  # Reverse a random word

        # Add informal phrases or human-like quirks
        if random.random() < 0.4:  # 40% chance to add quirks
            words.insert(random.randint(0, len(words) - 1), "Well,")  # Insert an informal phrase

        humanized_sentences.append(' '.join(words))
    
    return ' '.join(humanized_sentences)

def add_personal_touches(text):
    additional_phrases = [
        "I once had a situation where",
        "From my own experience,",
        "A memorable experience was",
        "Interestingly,",
        "One time, I noticed that"
    ]

    sentences = sent_tokenize(text)
    enhanced_sentences = []

    for sentence in sentences:
        if random.random() < 0.5:  # 50% chance to add a personal touch
            sentence = random.choice(additional_phrases) + " " + sentence
        enhanced_sentences.append(sentence)
    
    return ' '.join(enhanced_sentences)

def post_process_text(text):
    # Remove typical AI patterns and adjust tone
    text = re.sub(r'\b(you|your)\b', 'one', text)  # Change formal address to informal
    text = re.sub(r'\b([A-Z][a-z]*\s)*\b', lambda x: x.group().capitalize(), text)  # Capitalize proper nouns
    text = re.sub(r'\b(need|want|must)\b', 'gotta', text)  # Use colloquial expressions
    text = re.sub(r'\b(very|really)\b', '', text)  # Remove or replace intensifiers
    text = re.sub(r'\b(therefore|thus)\b', 'so', text)  # Simplify formal connectors
    text = re.sub(r'\b(\w+ing)\b', lambda x: x.group().replace('ing', 'in'), text)  # Alter verb endings
    
    # Add human-like inconsistencies
    text = re.sub(r'\b(I am)\b', 'I’m', text)  # Contract verbs
    text = re.sub(r'\b([A-Za-z]+ed\b)', lambda x: x.group() + " (once)", text)  # Add parentheses for verbs
    
    # Further randomize to avoid AI detection
    text = re.sub(r'\b([a-zA-Z]+)\b', lambda x: x.group() + random.choice(['', '.']), text)  # Add random punctuation

    return text

def manual_edit(text):
    # Function for manual review and adjustment
    text = re.sub(r'\b(somehow|anyway|you know)\b', '', text)  # Remove filler words
    text = re.sub(r'\b(I)\b', 'One', text, count=2)  # Change perspective for variability
    return text

# Generate initial content
prompt = "Write a blog post about how AI will work for future SEO."
initial_content = generate_initial_content(prompt)

# Humanize the text
humanized_content = humanize_text(initial_content)

# Add personal touches
personalized_content = add_personal_touches(humanized_content)

# Post-process the text
processed_content = post_process_text(personalized_content)

# Manual edit to add final human-like touches
final_content = manual_edit(processed_content)

# Print the final content
print(final_content)
