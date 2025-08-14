from django.contrib import admin
from .models import Company, CompanyMember

# This defines an "inline" view for CompanyMember,
# which allows us to edit members from the Company page.
class CompanyMemberInline(admin.TabularInline):
    model = CompanyMember
    extra = 1  # How many empty forms to show for adding new members
    autocomplete_fields = ['user']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    inlines = [CompanyMemberInline]

@admin.register(CompanyMember)
class CompanyMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role')
    list_filter = ('role', 'company')
    search_fields = ('user__email', 'company__name')