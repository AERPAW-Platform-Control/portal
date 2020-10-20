
# Register your models here.

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ResourceCreateForm, ResourceChangeForm
from .models import Resource


class AerpawResourceAdmin(admin.ModelAdmin):
    add_form = ResourceCreateForm
    form = ResourceChangeForm
    model = Resource
    list_display = ['name', 'description', 'resourceType', 'units', 'location', 'admin']


admin.site.register(Resource, AerpawResourceAdmin)