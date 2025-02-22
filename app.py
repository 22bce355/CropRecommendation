from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os

default_prompt = "You are a helpful AI chatbot providing agricultural assistance."

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you set this in your environment

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        user_message = data.get("queryText", "")

        if not user_message:
            return jsonify({"error": "Empty query text"}), 400

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": default_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"fulfillmentText": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
