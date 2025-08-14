# In users/models.py

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User Model for the Rent Management App.
    Uses email as the primary identifier instead of username.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Roles(models.TextChoices):
        LANDLORD = 'LANDLORD', 'Landlord'
        TENANT = 'TENANT', 'Tenant'
        # Let's add a more specific role for this case
        CORPORATE_TENANT = 'CORPORATE_TENANT', 'Corporate Tenant' 
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'



    # AbstractUser already has username, password, first_name, last_name, etc.
    # We will use the email field for login.
    email = models.EmailField(
        'email address',
        unique=True, # Make email the unique identifier
        help_text='Required. Used for login and notifications.'
    )

    phone_number = models.CharField(
            max_length=20,
            unique=True,
            null=True, # Make it nullable for now, as existing users won't have it
            blank=True,
            help_text="User's phone number, including country code (e.g., +14155552671)"
        )

    # Add your custom fields directly to the User model
    role = models.CharField(
        max_length=50,
        choices=Roles.choices,
        default=Roles.USER
    )
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(default=False)

    companies = models.ManyToManyField(
        'companies.Company',
        through='companies.CompanyMember',
        related_name='members'
        
    )
    
    # This tells Django to use the email field as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    
    # We must keep 'username' here because AbstractUser requires it, 
    # but we can make it non-unique and not required for registration.
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"