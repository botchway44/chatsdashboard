
import hashlib
import hmac
import requests

from datetime import datetime, timezone

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status

# Import the models we need to interact with
from users.models import User
from chats.models import ChatMessage
from .serializers import SendMessageSerializer, ChatMessageSerializer



class Dialog360WebhookView(APIView):
    """
    Handles incoming webhooks from the 360dialog platform.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def _verify_signature(self, request):
        # ... (This function remains unchanged) ...
        signature_header = request.headers.get('X-Hub-Signature-256')
        if not signature_header:
            return False
        signature_parts = signature_header.split('=')
        if len(signature_parts) != 2:
            return False
        algorithm, signature = signature_parts
        if algorithm != 'sha256':
            return False
        secret = settings.DIALOG_360_WEBHOOK_SECRET.encode('utf-8')
        mac = hmac.new(secret, msg=request.body, digestmod=hashlib.sha256)
        expected_signature = mac.hexdigest()
        return hmac.compare_digest(signature, expected_signature)

    def post(self, request, *args, **kwargs):
        # if not self._verify_signature(request):
            # return Response({"error": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        print("Received valid webhook data:", data)

        try:
            # --- This is the new logic for handling incoming messages ---
            if 'entry' in data and data['entry']:
                for entry in data['entry']:
                    for change in entry.get('changes', []):
                        value = change.get('value', {})
                        
                        # Handle incoming messages from a user
                        if 'messages' in value:
                            for message in value['messages']:
                                sender_phone_number = f"+{message['from']}"
                                message_content = message.get('text', {}).get('body')
                                timestamp_str = message.get('timestamp')
                                wamid = message.get('id')

                                if not message_content:
                                    continue # Skip if there's no text content

                                # Find the user associated with this phone number
                                try:
                                    user = User.objects.get(phone_number=sender_phone_number)
                                except User.DoesNotExist:
                                    print(f"No user found with phone number: {sender_phone_number}")
                                    # Optional: Handle messages from unknown numbers, e.g., create a lead
                                    user = None
                                
                                # Convert timestamp to a datetime object
                                timestamp = datetime.fromtimestamp(int(timestamp_str), tz=timezone.utc)

                                # Create the chat message in our database
                                ChatMessage.objects.create(
                                    user=user,
                                    wamid=wamid,
                                    content=message_content,
                                    timestamp=timestamp,
                                    direction=ChatMessage.MessageDirection.INBOUND,
                                    channel='whatsapp',
                                    status=ChatMessage.MessageStatus.DELIVERED # Mark as delivered since we received it
                                )

                        # Handle status updates for messages we sent
                        if 'statuses' in value:
                            for status_update in value['statuses']:
                                wamid = status_update.get('id')
                                message_status_text = status_update.get('status')

                                # Find the message we sent and update its status
                                try:
                                    message_to_update = ChatMessage.objects.get(wamid=wamid)
                                    message_to_update.status = message_status_text.upper() # e.g., 'SENT', 'DELIVERED', 'READ'
                                    message_to_update.save()
                                except ChatMessage.DoesNotExist:
                                    print(f"Received status for an unknown message WAMID: {wamid}")

        except Exception as e:
            # Log any unexpected errors during processing
            print(f"Error processing webhook data: {e}")
            # Still return a 200 OK so the service doesn't keep retrying
            
        return Response(status=status.HTTP_200_OK)
    
    


class SendMessageView(generics.GenericAPIView):
    """
    API view to send a new message via the 360dialog API.
    """
    serializer_class = SendMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        to_number = serializer.validated_data['to_number']
        message_body = serializer.validated_data['message_body']

        # Construct the payload for the 360dialog API
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_number,
            "type": "text",
            "text": { "body": message_body }
        }

        headers = {
            "D360-API-KEY": settings.DIALOG_360_WEBHOOK_SECRET,
            "Content-Type": "application/json"
        }
        
        api_url = "https://waba-sandbox.360dialog.io/v1/messages"

        try:
            # Make the API call to 360dialog
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status() # Raises an exception for bad status codes (4xx or 5xx)
            
            response_data = response.json()
            message_wamid = response_data['messages'][0]['id']

            # Find the user we are sending the message to
            recipient_user = User.objects.filter(phone_number=f"+{to_number}").first()

            # Log the outgoing message in our database
            ChatMessage.objects.create(
                user=recipient_user,
                wamid=message_wamid,
                content=message_body,
                timestamp=datetime.now(tz=timezone.utc),
                direction=ChatMessage.MessageDirection.OUTBOUND,
                status=ChatMessage.MessageStatus.SENT,
                channel='whatsapp'
            )

            return Response({"status": "Message sent successfully", "wamid": message_wamid}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            # Handle potential network errors or bad responses from 360dialog
            print(f"Error sending message to 360dialog: {e}")
            return Response({"error": "Failed to send message via provider"}, status=status.HTTP_502_BAD_GATEWAY)
        

class ChatMessageListView(generics.ListAPIView):
    """
    API view to retrieve a paginated list of chat messages
    for the currently authenticated user.
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This method is the key to security. It ensures that users can only ever
        see their own messages by filtering the ChatMessage objects based on
        the logged-in user.
        """
        return ChatMessage.objects.filter(user=self.request.user)

