import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Crucial: Allows your website to talk to this backend

# 1. Setup Gemini (API Key will be set in Render/Local Env)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Load your resume data
with open("resume_data.txt", "r") as f:
    resume_context = f.read()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # The "System Prompt" tells the AI how to behave
    prompt = f"""
    You are an AI assistant representing a student. 
    Use the following resume context to answer the user's question. 
    If the answer isn't in the context, say you're not sure but offer to 
    provide the student's email. Keep answers professional and brief.

    Context: {resume_context}
    User Question: {user_message}
    """
    
    response = model.generate_content(prompt)
    return jsonify({"response": response.text})

if __name__ == '__main__':
    # Use the PORT provided by Render, or default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    # Must use 0.0.0.0 to let Render's network in
    app.run(host='0.0.0.0', port=port)