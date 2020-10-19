from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ResourcesCreationForm, ResourcesChangeForm
from .models import Resources


class AerpawResourceAdmin(UserAdmin):
    add_form = ResourcesCreationForm
    form = ResourcesChangeForm
    model = Resources
    list_display = ['name', 'resourceType', 'units', 'location', 'oidc_claim_sub']


admin.site.register(Resources, AerpawUserAdmin)