from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ResourcesCreateForm, ResourcesChangeForm
from .models import Resources


class AerpawResourceAdmin():
    add_form = ResourcesCreateForm
    form = ResourcesChangeForm
    model = Resources
    list_display = ['name', 'description', 'resourceType', 'units', 'location', 'admin']


admin.site.register(Resources, AerpawResourceAdmin)