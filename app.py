from flask import Flask, render_template, request, jsonify
from chatbot.model import generate_response_from_groq
from utils.subtitles import get_subtitles
import os

app = Flask(__name__)

#-------
from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from utils.subtitles import *     # AI subtitles if used
from chatbot.model import *       # Any AI model logic

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Config
app.config['MONGO_URI'] = 'mongodb://localhost:27017/english_learning'
mongo = PyMongo(app)

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/index')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['user'] = email
            return redirect('/index')
        return redirect('/login')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        mongo.db.users.insert_one({'email': email, 'password': password})
        return redirect('/login')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html')  # your media player UI
    return redirect('/login')

#---------

# @app.route('/')
# def index():
#     return render_template('index.html')

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
