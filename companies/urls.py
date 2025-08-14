from django.urls import path
from .views import AdminCompanyListView, CompanyCreateView

urlpatterns = [
    path('', CompanyCreateView.as_view(), name='company-create'),
    path('all/', AdminCompanyListView.as_view(), name='company-list-all'), # Add this line

]