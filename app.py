import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# USE THIS EXACT MODEL NAME
model = genai.GenerativeModel('gemini-flash-latest')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        
        # Load resume (safely)
        try:
            with open("resume_data.txt", "r") as f:
                resume_context = f.read()
        except FileNotFoundError:
            resume_context = "Resume data unavailable."

        prompt = f"""
        You are an AI assistant representing Nicholas Weng. 
        Context: {resume_context}
        User Question: {user_message}
        """
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"response": "I'm having trouble connecting. Please try again later."}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)