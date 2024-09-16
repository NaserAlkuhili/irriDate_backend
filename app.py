import os
from flask import Flask, request, jsonify
from model import predict
from notifications import send_push_notification

app = Flask(__name__)

@app.route('/')
def index():
    return "Service is up and running!"

@app.route('/predict', methods=['POST'])
def predict_and_notify():
    try:
        data = request.json
        input_value = float(data.get('input_value'))  # Convert input to float
        expo_push_token = data.get('expo_push_token')

        if input_value is None or expo_push_token is None:
            raise ValueError("Missing input_value or expo_push_token")

        prediction = predict(input_value)  # This returns a native int

        if prediction == 1:
            send_push_notification(expo_push_token)
            return jsonify({'prediction': prediction, 'notification_sent': True})
        else:
            return jsonify({'prediction': prediction, 'notification_sent': False})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)
