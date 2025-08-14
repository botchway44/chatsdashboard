import uuid
from django.db import models
from django.conf import settings

from users.models import User

class ChatMessage(models.Model):
    class MessageDirection(models.TextChoices):
        INBOUND = 'INBOUND', 'Inbound'   # From user to us
        OUTBOUND = 'OUTBOUND', 'Outbound' # From us to user

    class MessageStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SENT = 'SENT', 'Sent'
        DELIVERED = 'DELIVERED', 'Delivered'
        READ = 'READ', 'Read'
        FAILED = 'FAILED', 'Failed'

    # --- Core Fields ---
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField()

    # --- Tracking & Metadata ---
    channel = models.CharField(max_length=50, default='whatsapp')
    direction = models.CharField(max_length=10, choices=MessageDirection.choices)
    status = models.CharField(
        max_length=10,
        choices=MessageStatus.choices,
        default=MessageStatus.PENDING
    )
    
    # --- External IDs for Webhook Tracking ---
    wamid = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text="WhatsApp Message ID for tracking status updates"
    )
    
    # Timestamps for our own records
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Check if a user is associated with this message
        user_identifier = self.user.email if self.user else "Unknown User"
        
        # Use the safe identifier in the string
        return f"Message {self.direction} for {user_identifier}"

    class Meta:
        ordering = ['timestamp']