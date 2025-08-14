from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the ChatMessage model.
    """
    
    # --- List View Customization ---
    list_display = (
        'user',
        'direction',
        'status',
        'channel',
        'timestamp',
        'get_content_preview' # A custom method to show a short preview
    )
    list_filter = ('status', 'direction', 'channel', 'timestamp')
    search_fields = ('user__email', 'user__username', 'content', 'wamid')

    # --- Detail View Customization ---
    readonly_fields = ('id', 'wamid', 'created_at', 'timestamp')
    
    fieldsets = (
        ('Message Details', {
            'fields': ('id', 'user', 'direction', 'status', 'channel')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Metadata', {
            'fields': ('wamid', 'timestamp', 'created_at')
        }),
    )

    @admin.display(description='Content Preview')
    def get_content_preview(self, obj):
        # Returns the first 50 characters of the message content
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content