from flask import Flask, request, jsonify
from model import predict
from notifications import send_push_notification

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_and_notify():
    try:
        # Get the input data from the request
        data = request.json
        input_value = float(data.get('input_value'))  # Convert input to float
        expo_push_token = data.get('expo_push_token')

        if input_value is None or expo_push_token is None:
            raise ValueError("Missing input_value or expo_push_token")

        # Predict the outcome using the model
        prediction = predict(input_value)  # This returns a native int

        # If the model predicts 1, send a push notification
        if prediction == 1:
            send_push_notification(expo_push_token)
            return jsonify({'prediction': prediction, 'notification_sent': True})
        else:
            return jsonify({'prediction': prediction, 'notification_sent': False})
    
    except Exception as e:
        # Log the error for debugging and return a JSON response with the error message
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
