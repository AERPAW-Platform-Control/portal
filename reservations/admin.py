from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ReservationCreateForm, ReservationChangeForm
from .models import Reservation


class AerpawReservationAdmin(admin.ModelAdmin):
    add_form = ReservationCreateForm
    form = ReservationCreateForm
    model = Reservation
    list_display = ['name', 'description', 'state', 'start_date', 'end_date','experiment','resource']


admin.site.register(Reservation, AerpawReservationAdmin)