from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ExperimentCreateForm, ExperimentUpdateForm
from .models import Experiment


class AerpawExperimentAdmin(admin.ModelAdmin):
    add_form = ExperimentCreateForm
    form = ExperimentCreateForm
    model = Experiment
    list_display = ['name', 'description', 'stage', 'created_by', 'created_date','project']


admin.site.register(Experiment, AerpawExperimentAdmin)