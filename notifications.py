import requests

# Function to send a push notification via Expo API
def send_push_notification(expo_push_token):
    message = {
        'to': expo_push_token,
        'sound': 'default',
        'title': 'AI Model Alert',
        'body': 'Your AI model predicted 1!',
    }
    response = requests.post(
        'https://exp.host/--/api/v2/push/send',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        json=message,
    )
    print(response)
    return response.status_code
