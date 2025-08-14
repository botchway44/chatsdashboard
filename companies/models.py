import uuid
from django.db import models
from common.models import BaseModel
from django.conf import settings

class Company(BaseModel):

    # Other fields for the Company model
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CompanyMember(BaseModel):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        VIEWER = 'VIEWER', 'Viewer'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.MANAGER)

    class Meta:
        unique_together = ('user', 'company') # A user can only have one role per company

    def __str__(self):
        return f"{self.user.email} in {self.company.name} as {self.get_role_display()}"