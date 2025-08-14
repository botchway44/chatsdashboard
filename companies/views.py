# companies/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .permissions import IsAdminUser
from .models import Company, CompanyMember
from .serializers import CompanySerializer

class CompanyCreateView(generics.CreateAPIView):
    """
    API view for creating a new company.
    The user who creates the company is automatically made an admin.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated] # Only logged-in users can create a company

    def perform_create(self, serializer):
        # Step 1: Save the new company instance
        company = serializer.save()

        # Step 2: Create the link between the user and the new company
        CompanyMember.objects.create(
            company=company,
            user=self.request.user,
            role=CompanyMember.Roles.ADMIN
        )

class AdminCompanyListView(generics.ListAPIView):
    """
    API view for admins to retrieve a list of all companies.
    """
    queryset = Company.objects.all().order_by('-created_at')
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser] # Use our custom admin-only permission