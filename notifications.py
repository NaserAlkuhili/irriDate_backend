import requests

# Function to send a push notification via Expo API
def send_push_notification(expo_push_token):
    message = {
        'to': expo_push_token,
        'sound': 'default',
        'title': 'Your Palm Trees Need Water 🌴💧',
        'body': 'Please water your plants',
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
