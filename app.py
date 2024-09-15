from flask import Flask, request, jsonify
from model import predict
from notifications import send_push_notification

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_and_notify():
    data = request.json
    input_value = data['input_value']
    expo_push_token = data['expo_push_token']

    # Predict the outcome
    prediction = predict(input_value)
    
    if prediction == 1:
        # Send push notification if the model returns 1
        send_push_notification(expo_push_token)
        return jsonify({'prediction': prediction, 'notification_sent': True})
    else:
        return jsonify({'prediction': prediction, 'notification_sent': False})

if __name__ == '__main__':
    app.run(debug=True)
