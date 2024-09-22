# import os
# from flask import Flask, request, jsonify
# from model import predict
# from notifications import send_push_notification

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return "Service is up and running!"

# @app.route('/predict', methods=['POST'])
# def predict_and_notify():
#     try:
#         data = request.json
#         input_value = data.get('input_value')  # Get the input as a list
#         expo_push_token = data.get('expo_push_token')

#         if input_value is None or expo_push_token is None:
#             raise ValueError("Missing input_value or expo_push_token")

#         # Ensure the input_value is a list and contains three items
#         if not isinstance(input_value, list) or len(input_value) != 3:
#             raise ValueError("input_value must be a list with three values")

#         # Predict the outcome using the model
#         prediction = predict(input_value)  # This returns a native int

#         if prediction == 1:
#             send_push_notification(expo_push_token)
#             return jsonify({'prediction': prediction, 'notification_sent': True})
#         else:
#             return jsonify({'prediction': prediction, 'notification_sent': False})

#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
#     app.run(host='0.0.0.0', port=port, debug=True)


import os
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from model import predict
from notifications import send_push_notification

app = Flask(__name__)

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
        input_value = data.get('input_value')  # Get the input as a list
        expo_push_token = data.get('expo_push_token')

        if input_value is None or expo_push_token is None:
            raise ValueError("Missing input_value or expo_push_token")

        # Ensure the input_value is a list and contains three items
        if not isinstance(input_value, list) or len(input_value) != 3:
            raise ValueError("input_value must be a list with three values")

        # Predict the outcome using the existing model
        prediction = predict(input_value)  # This returns a native int

        if prediction == 1:
            send_push_notification(expo_push_token)
            return jsonify({'prediction': prediction, 'notification_sent': True})
        else:
            return jsonify({'prediction': prediction, 'notification_sent': False})

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

        # Preprocess the image for the model
        img = image.load_img(img_file, target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0  # Normalize the image
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Make prediction using the plant health model
        predictions = plant_health_model.predict(img_array)
        probabilities = predictions[0].tolist()

        # Return the prediction result
        return jsonify({'prediction': probabilities})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get the port from the environment variable or fallback to 5001 for local development
    port = int(os.environ.get('PORT', 5001))  # Use Render's dynamic port or 5001 locally
    print(f"Running on port {port}")
    app.run(host='0.0.0.0', port=port)


