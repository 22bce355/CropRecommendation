from flask import Flask, request, jsonify

app = Flask(__name__)

# Crop recommendations based on soil type
crop_recommendations = {
    "sandy": ["Watermelon", "Peanuts", "Millets"],
    "clay": ["Rice", "Jute", "Tomato"],
    "loamy": ["Wheat", "Sugarcane", "Vegetables"],
    "black": ["Cotton", "Soybean", "Sunflower"]
}

@app.route('/')
def home():
    return "Crop Recommendation Webhook is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract parameters from Dialogflow
    soil_type = req.get('queryResult', {}).get('parameters', {}).get('soiltype', '').lower()
    season = req.get('queryResult', {}).get('parameters', {}).get('season', '').lower()

    if soil_type and season:
        crops = crop_recommendations.get(soil_type, [])
        
        if crops:
            fulfillment_text = f"For {soil_type} soil in {season}, you can grow: {', '.join(crops)}."
        else:
            fulfillment_text = f"Sorry, I don’t have recommendations for {soil_type} soil."
    else:
        fulfillment_text = "Please provide both soil type and season for recommendations."

    return jsonify({'fulfillmentText': fulfillment_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
