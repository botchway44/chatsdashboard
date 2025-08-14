# chat/serializers.py

from rest_framework import serializers

from chats.models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        # Define the fields you want to include in the API response
        fields = [
            'id', 
            'content', 
            'timestamp', 
            'direction', 
            'status', 
            'wamid', 
            'created_at'
        ]


class SendMessageSerializer(serializers.Serializer):
    to_number = serializers.CharField(max_length=20)
    message_body = serializers.CharField()