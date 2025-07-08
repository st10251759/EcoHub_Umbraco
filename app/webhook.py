from flask import Blueprint, request, jsonify
import os
import requests
import json

webhook_bp = Blueprint('webhook', __name__)

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

@webhook_bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification for WhatsApp
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("Webhook verified successfully!")
                return challenge
            else:
                print("Webhook verification failed!")
                return 'Forbidden', 403
    
    elif request.method == 'POST':
        # Handle incoming WhatsApp messages
        data = request.get_json()
        
        print(f"Received webhook data: {json.dumps(data, indent=2)}")
        
        # Extract message information
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if 'value' in change and 'messages' in change['value']:
                            messages = change['value']['messages']
                            for message in messages:
                                phone_number = message['from']
                                message_text = message.get('text', {}).get('body', '')
                                
                                print(f"Message from {phone_number}: {message_text}")
                                
                                # Process the message and send response
                                process_message(phone_number, message_text)
        
        return jsonify({"status": "success"}), 200

def process_message(phone_number, message_text):
    """Process incoming message and send appropriate response"""
    
    # Simple response logic (you'll expand this later)
    if 'hello' in message_text.lower() or 'hi' in message_text.lower():
        response = "Hello! Welcome to Busamed Service Desk. How can I help you today?"
    elif 'ticket' in message_text.lower():
        response = "I can help you log a new ticket. Please describe your issue."
    elif 'help' in message_text.lower():
        response = "I can help you with:\n1. Log a new ticket\n2. Check ticket status\n3. Get general help\n\nWhat would you like to do?"
    else:
        response = "Thank you for your message. I'm the Busamed Service Desk chatbot. Type 'help' to see what I can do."
    
    # Send response back to user
    send_whatsapp_message(phone_number, response)

def send_whatsapp_message(phone_number, message):
    """Send a message via WhatsApp Cloud API"""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {"body": message}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Message sent successfully: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None