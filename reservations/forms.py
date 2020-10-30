from django import forms

from accounts.models import AerpawUser
from experiments.models import Experiment
from .models import Reservation
from resources.models import Resource

class ReservationCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Resource Name',
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Resource Description',
    )
    
    resource = forms.ModelChoiceField(
        queryset=Resource.objects.order_by('name'),
        required=True,
        widget=forms.Select(),
        label='Resource',
    )

    units = forms.IntegerField(
        required=True,
        initial=0,
        widget=forms.NumberInput(),
        label='Resource Units',
    )

    class Meta:
        model = Reservation
        fields = (
            'name',
            'description',
            'resource',
            'units',
            'start_date',
            'end_date',
        )


class ReservationChangeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Resource Description',
    )

    resource = forms.ModelChoiceField(
        queryset=Resource.objects.order_by('name'),
        required=False,
        widget=forms.Select(),
        label='Resource',
    )

    units = forms.IntegerField(
        required=True,
        initial=0,
        widget=forms.NumberInput(),
        label='Resource Units',
    )

    class Meta:
        model = Reservation
        fields = (
            'name',
            'description',
            'resource',
            'units',
            'start_date',
            'end_date',
        )
