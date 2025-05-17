import os
from groq import Groq
import requests

# Initialize the Groq client with your API key
api_key = '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'

client = Groq(api_key=api_key)

def generate_response_from_groq(prompt):

    try:
            # Create a chat completion
        chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an English tutor."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-70b-8192"  # Replace with your desired model
    )

        # Return the assistant's response
        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error getting response from Groq API: {e}"
