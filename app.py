import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # 1. Ask Google: "What models does this API key have access to?"
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # 2. Format the list as a string
        model_list_str = ", ".join(available_models)
        
        # 3. Send this list back to your website as the "AI Response"
        debug_message = f"DEBUG MODE. Your valid models are: {model_list_str}"
        
        return jsonify({"response": debug_message})

    except Exception as e:
        return jsonify({"response": f"Critical Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)