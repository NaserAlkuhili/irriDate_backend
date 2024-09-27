
import os
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from smart_irrigation_model import predict
from notifications import send_push_notification
from io import BytesIO
from PIL import Image 
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate('config/irridate-30465-firebase-adminsdk-8c1bt-eddec70618.json')
firebase_admin.initialize_app(cred)

# Firestore DB
db = firestore.client()

# Try loading the plant health model and handle any errors
try:
    plant_health_model = load_model('models/palm_tree_health_model.h5')
    print("Plant health model loaded successfully.")
except Exception as e:
    print(f"Error loading plant health model: {str(e)}")

@app.route('/')
def index():
    return "Service is up and running!"

# Existing route for the other model
@app.route('/predict', methods=['POST'])
def predict_and_notify():
    try:
        data = request.json
        input_value = data['input_value']
        temperature = input_value[0]
        moisture_level = input_value[1]

        expo_push_token = data['expo_push_token']

        if None in [temperature, moisture_level, expo_push_token]:
            raise ValueError("Missing temperature, moisture_level, or expo_push_token")

        # Query the Firestore 'users' collection using the expo_push_token
        user_ref = db.collection('users').where('expoPushToken', '==', expo_push_token).get()

        if not user_ref:
            raise ValueError(f"No user found with expo_push_token: {expo_push_token}")

        # Assume there's only one document matching this token
        user_doc = user_ref[0]
        user_data = user_doc.to_dict()

        # Get the growthStage from the user's document
        growth_stage = user_data.get('growthStage', 1)  # Default to 1 if not found
        print(f'growth_stage: {growth_stage}')
        print('----' * 100)

        # Prepare the input_value list from the sensor data
        input_value = [temperature, moisture_level, growth_stage]

        # Predict the outcome using the existing model
        prediction = predict(input_value)

        # Send notification if prediction is 1
        if prediction == 1:
            send_push_notification(expo_push_token)

        # Updating the 'data' field in the user's document with the new sensor data
        # Get the current 'data' array (if exists) from the user document
        current_data = user_data.get('data', [])

        # Ensure the array doesn't exceed 5 elements (delete the oldest if needed)
        if len(current_data) >= 5:
            current_data.pop(0)  # Remove the oldest entry (first element)

        # Append the new data (temperature, moisture_level, time)
        new_entry = {
            'temperature': temperature,
            'moisture_level': moisture_level,
        }
        current_data.append(new_entry)

        # Update the 'data' array in the user's document
        db.collection('users').document(user_doc.id).update({
            'data': current_data
        })

        return jsonify({'prediction': prediction, 'notification_sent': prediction == 1})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

# New route for the palm tree health model
@app.route('/predict_plant_health', methods=['POST'])
def predict_plant_health():
    try:
        # Get the image file from the request
        img_file = request.files.get('image')
        if img_file is None:
            raise ValueError("No image file provided")

        # Open the image and ensure it is in RGB format (remove alpha channel if present)
        img = Image.open(BytesIO(img_file.read())).convert('RGB')  # Convert to RGB

        # Preprocess the image for the model
        img = img.resize((256, 256))  # Resize to match model input size
        img_array = np.expand_dims(img, axis=0)  # Add batch dimension

        # Make prediction using the plant health model
        predictions = plant_health_model.predict(img_array)
        probabilities = predictions[0].tolist()

        # Return the prediction result
        return jsonify({'prediction': probabilities})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Get the port from the environment variable or fallback to 5001 for local development
    port = int(os.environ.get('PORT', 5001))  # Use Render's dynamic port or 5001 locally
    print(f"Running on port {port}")
    app.run(host='0.0.0.0', port=port)


