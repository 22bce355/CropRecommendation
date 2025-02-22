from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "Crop Recommendation Webhook is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print("Received Request:", req)  # Debugging

    # Extract user query from Dialogflow request
    user_query = req.get('queryResult', {}).get('queryText', '')

    if user_query:
        # Send the entire user query to OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant specializing in crop recommendations."},
                {"role": "user", "content": user_query}
            ]
        )

        fulfillment_text = response["choices"][0]["message"]["content"].strip()
    else:
        fulfillment_text = "I'm sorry, but I couldn't understand your query."

    print(f"Response Sent: {fulfillment_text}")  # Debugging
    return jsonify({'fulfillmentText': fulfillment_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
