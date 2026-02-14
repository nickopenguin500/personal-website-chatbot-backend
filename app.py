import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure API Key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# --- DIAGNOSTIC ROUTE ---
@app.route('/models', methods=['GET'])
def list_models():
    try:
        model_list = []
        for m in genai.list_models():
            # We only care about models that support 'generateContent'
            if 'generateContent' in m.supported_generation_methods:
                model_list.append(m.name)
        return jsonify({"available_models": model_list})
    except Exception as e:
        return jsonify({"error": str(e)})

# --- MAIN CHAT ROUTE ---
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        # Load resume (safely)
        if os.path.exists("resume_data.txt"):
            with open("resume_data.txt", "r") as f:
                resume_context = f.read()
        else:
            resume_context = "Resume data not found."

        prompt = f"""
        You are an AI assistant representing a student. 
        Context: {resume_context}
        User Question: {user_message}
        """

        # --- THE FIX MIGHT BE HERE ---
        # We will try a fallback strategy. 
        # If 1.5-flash fails, we try 'gemini-pro' (older but reliable)
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
        except Exception:
            # Fallback to the most standard model
            print("Switching to fallback model: gemini-pro")
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

        return jsonify({"response": response.text})

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"response": f"Backend Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)