### Endpoints
* `POST /chat`: Accepts a JSON object `{"message": "string"}`. Returns a JSON response with the AI's answer based on my resume.

### Frontend Communication
The frontend sends user queries via the `fetch` API. It displays the returned string in the chat window.

### Local Setup
1. Install requirements: `pip install -r requirements.txt`
2. Set Environment Variable: `export GEMINI_API_KEY='your_key'`
3. Run: `python app.py`

### Security
API keys are handled via Render Environment Variables. No secrets are stored in the repository.

### Prompt Log
* **Model used:** Gemini 1.5 Flash
* **Key Prompt:** "You are an AI assistant representing a student. 
    Use the following resume context to answer the user's question. 
    If the answer isn't in the context, say you're not sure but offer to 
    provide the student's email. Keep answers professional and brief."

### Prompt History:
(Multiple prompts asking for suggestions)
1. im thinking maybe an AI chatbot for my personal website, but I'm worried that it'll say some untrue things when actually used
(Lots of debugging with using Gemini's API keys)
2. wait i want to add this to my existing website on github pages, could you go back over phase 1? I will upload my website files here
3. ok wait before we move to phase 4, how do i check that this works
4. 