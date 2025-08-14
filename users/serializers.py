from rest_framework import serializers
from .models import User


# This serializer is for DISPLAYING user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # List the fields you want to return to the frontend
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password', style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'role')
        extra_kwargs = {
            'username': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', User.Roles.LANDLORD)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user