from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Your Gemini API Key
GEMINI_API_KEY = "AIzaSyDqSJrWmj9RmEMMKoIP1CiL9ROY6PWreI0"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'BEKON AI API is running!', 'status': 'online'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400
        
        message = data.get('message', '')
        if not message:
            return jsonify({'error': 'No message'}), 400
        
        response = model.generate_content(message)
        return jsonify({'response': response.text})
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400
        
        answers = data.get('answers', [])
        if not answers:
            return jsonify({'error': 'No answers'}), 400
        
        combined = ' '.join(answers)
        
        prompt = f"""You are a career counselor for Ethiopian students. Analyze these childhood experiences and suggest career paths:

{combined}

Give 3 department recommendations with Ethiopian universities."""
        
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
        
    except Exception as e:
        print(f"Analyze error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
