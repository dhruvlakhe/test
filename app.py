import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Replace 'YOUR_ACCESS_TOKEN' with your actual access token from Meta Developers
ACCESS_TOKEN = 'EAAFmfsD78IYBO4F95PXRbS0mbnZCP7C4UwQytnE3cYTh2sTXFSlJwTC9ZB754hoibBnwJMWQXNoeC54pDvxuyuZBcjEMgEHwVPym5spFZCRXolyGds9n7zSOdqvhxLsCIWtBanWS44otQjnEnX2j5I57Ys3wvWIwRgUMXNGlt8cC3XW5gExUuAnTMTgRGSKZBuZBFR9QTvBPfsslKAliBZAy6g2PucZD'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification challenge response
        return request.args.get('hub.challenge')
    elif request.method == 'POST':
        data = request.get_json()
        handle_incoming_message(data)
        return jsonify({'status': 'received'}), 200

def handle_incoming_message(data):
    for entry in data.get('entry', []):
        for message_event in entry.get('changes', []):
            message = message_event.get('value', {}).get('messages', [])[0]
            if message:
                sender_id = message['from']
                message_text = message.get('text', {}).get('body', '')

                # Basic keyword-based logic
                if 'hello' in message_text.lower():
                    response_text = 'Hi there! How can I assist you today?'
                elif 'help' in message_text.lower():
                    response_text = 'Sure, I am here to help! What do you need assistance with?'
                elif 'bye' in message_text.lower():
                    response_text = 'Goodbye! Have a great day!'
                else:
                    response_text = 'I am not sure how to respond to that. Can you please rephrase?'

                # Send the response back to the user
                send_message(sender_id, response_text)

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v13.0/me/messages?access_token={ACCESS_TOKEN}"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'messaging_product': 'whatsapp',
        'to': recipient_id,
        'text': {'body': message_text}
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Response: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(debug=True)
