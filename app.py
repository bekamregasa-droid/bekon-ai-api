from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyDqSJrWmj9RmEMMKoIP1CiL9ROY6PWreI0")
model = genai.GenerativeModel('gemini-pro')

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'online'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        response = model.generate_content(message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        combined = ' '.join(answers)
        response = model.generate_content(f"Analyze: {combined}")
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
