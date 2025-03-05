from flask import Flask, request, jsonify
import joblib
from twilio.rest import Client

app = Flask(__name__)

# Load AI Model
model = joblib.load("HAB_predictor.pkl")

import os
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
FISHERMAN_PHONE_NUMBER = os.getenv("FISHERMAN_PHONE_NUMBER")


# Function to send SMS alerts
def send_sms(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=FISHERMAN_PHONE_NUMBER)
@app.route('/')
def home():
    return "Welcome to the HAB Prediction API! Use /predict to send requests."

# API Route for Prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = [data['NDVI'], data['FAI'], data['Chlorophyll']]
    prediction = model.predict([features])

    if prediction[0] == 1:
        send_sms("⚠️ HAB Warning: Avoid fishing!")

    return jsonify({'HAB Risk': "High" if prediction[0] == 1 else "Safe"})

# Start Flask Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
