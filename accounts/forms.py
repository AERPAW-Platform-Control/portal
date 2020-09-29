# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AerpawUser


class AerpawUserCreationForm(UserCreationForm):

    class Meta:
        model = AerpawUser
        fields = ('username', 'email', 'first_name', 'last_name', 'oidc_claim_sub')


class AerpawUserChangeForm(UserChangeForm):

    class Meta:
        model = AerpawUser
        fields = ('username', 'email', 'first_name', 'last_name', 'oidc_claim_sub')
