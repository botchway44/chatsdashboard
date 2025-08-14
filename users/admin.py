from django.contrib import admin

# Register your models here.
from .models import  User

from django.contrib import admin


# class RoleInline(admin.TabularInline):
#     model = User.USER_ROLES
#     extra = 3


class UsersAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["email", "username","first_name","last_name","phone_number", "role"]}),
        ("Date information", {"fields": ["date_joined", "last_login"], "classes": ["collapse"]}),
    ]
    search_fields = ["email", "username"]
    list_filter = ["role", "date_joined"]
    # inlines = [RoleInline]
    list_display = ["email", "username","phone_number", "role", "date_joined", "last_login"]


admin.site.register(User, UsersAdmin)
# admin.site.register(User.Roles)