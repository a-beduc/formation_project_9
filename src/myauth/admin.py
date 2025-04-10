from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from myauth.models import User


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    """
    Custom admin configuration for the User model.
    """
    pass
