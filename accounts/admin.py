# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import AerpawUserCreationForm, AerpawUserChangeForm
from .models import AerpawUser


class AerpawUserAdmin(UserAdmin):
    add_form = AerpawUserCreationForm
    form = AerpawUserChangeForm
    model = AerpawUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'oidc_claim_sub']


admin.site.register(AerpawUser, AerpawUserAdmin)
