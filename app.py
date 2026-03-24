from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Your Gemini API Key
GEMINI_API_KEY = "AIzaSyDqSJrWmj9RmEMMKoIP1CiL9ROY6PWreI0"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'BEKON AI API is running!', 'status': 'online'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = model.generate_content(message)
        return jsonify({'response': response.text})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        
        if not answers:
            return jsonify({'error': 'No answers provided'}), 400
        
        prompt = f"""You are a career counselor for Ethiopian students. Analyze these childhood experiences:

{chr(10).join(answers)}

Provide:
1. Top 3 recommended departments at Ethiopian universities
2. Why each matches
3. Specific careers in each field
4. Ethiopian universities offering these programs
5. Encouraging next steps

Be detailed and specific to Ethiopia."""
        
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
