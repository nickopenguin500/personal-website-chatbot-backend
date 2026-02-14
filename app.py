import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. Configure Gemini with your API Key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Use a valid model from your list
# We selected 'gemini-2.0-flash' because it was in your debug output
model = genai.GenerativeModel('gemini-2.0-flash')

# 3. Load the resume data
# We use a try/except block to prevent crashing if the file is missing
try:
    with open("resume_data.txt", "r") as f:
        resume_context = f.read()
except FileNotFoundError:
    resume_context = "Resume data not found. Please contact the administrator."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        
        if not user_message:
            return jsonify({"response": "Please type a message."})

        # Create the prompt for the AI
        prompt = f"""
        You are an AI assistant representing Nicholas Weng. 
        Answer the user's question using ONLY the context below.
        If the answer isn't in the context, say you don't know but offer to 
        provide Nicholas's email (nicholasweng02@gmail.com). 
        Keep answers professional, friendly, and brief.

        Context: {resume_context}
        User Question: {user_message}
        """
        
        # Generate the response
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})

    except Exception as e:
        # If anything goes wrong, print the error to Render logs and tell the user
        print(f"ERROR: {e}")
        return jsonify({"response": "I'm having trouble connecting right now. Please try again later."}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)