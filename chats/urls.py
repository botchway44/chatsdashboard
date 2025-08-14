from django.urls import path
from .views import ChatMessageListView, Dialog360WebhookView, SendMessageView

urlpatterns = [
    path('360dialog/', Dialog360WebhookView.as_view(), name='webhook-360dialog'),
    path('send-message', SendMessageView.as_view(), name='send-message'),
    path('messages', ChatMessageListView.as_view(), name='message-list'), 

]