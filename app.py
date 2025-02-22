from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Prompts
default_prompt = "You are a helpful AI chatbot providing agricultural assistance."
crop_recommendation_prompt = (
    "You are an AI agricultural expert. Suggest suitable crops based on soil type, "
    "weather conditions, moisture, temperature, and climate."
)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        user_message = data.get("queryText", "").strip().lower()

        if not user_message:
            return jsonify({"error": "Empty query text"}), 400

        # Choose the appropriate prompt
        prompt = crop_recommendation_prompt if "crop recommendation" in user_message else default_prompt

        # Prepare the request payload
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 256
        }

        # Send request to Groq API
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"].strip()
            return jsonify({"fulfillmentText": reply})
        else:
            return jsonify({"error": f"Groq API error: {response.json()}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
