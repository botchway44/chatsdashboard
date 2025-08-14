from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from users.models import User
from users.serializers import UserRegisterSerializer, UserSerializer # Import UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve the details of the currently authenticated user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # The request.user is automatically populated by DRF and SimpleJWT
        # with the user associated with the provided token.
        return self.request.user
    
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully. Please check your email to verify your account."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )