# streamlit_app.py
import streamlit as st
import requests

# Backend API endpoint
api_url = 'http://127.0.0.1:5000/generate'

st.title('OpenAI Data Integration')
topic = st.text_input('Enter your topic:')
if st.button('Generate Content'):
    if topic:
        try:
            # Request content generation from the Flask backend
            response = requests.post(api_url, json={'topic': topic})
            if response.status_code == 200:
                response_json = response.json()
                if 'error' in response_json:
                    st.error(f"Error generating content: {response_json['error']}")
                else:
                    content = response_json['content']
                    st.success('Content generated and saved successfully!')
                    st.write(content)
            else:
                st.error(f"Failed to generate content: {response.status_code}")

        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
    else:
        st.warning('Please enter a topic.')
