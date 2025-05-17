from flask import Flask, render_template, request, jsonify
from chatbot.model import generate_response_from_groq
from utils.subtitles import get_subtitles

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subtitles', methods=['POST'])
def subtitles():
    data = request.json
    video_url = data.get('url')
    subtitles = get_subtitles(video_url)
    return jsonify(subtitles)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    word = data.get('word', '')
    sentence = data.get('sentence', '')

    prompt = f"""
You are a helpful and friendly English tutor for beginners.
The user clicked on a word in a transcript to understand it better.

The clicked word is: "{word}"
The full sentence is: "{sentence}"

Help the user understand this word and how to use it. 
Your response should be in this format:

---
🧠 Word: _{word}_

🔍 Meaning (General)  
Define the word simply for beginners.

💬 Meaning in This Sentence  
Explain what it means in the exact sentence context.

🧾 How to Use "{word}" in Real Life  
Give 2–3 real-life example sentences.

💡 Motivational Quotes  
Share 1–2 famous quotes using the word, if possible.

🌱 Final Tip  
Give a short motivational or encouraging tip related to learning or using this word.
---
"""
    
    # Send prompt to Groq API
    response = generate_response_from_groq(prompt)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
