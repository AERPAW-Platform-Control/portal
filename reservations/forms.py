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

    experiment = forms.ModelMultipleChoiceField(
        queryset=Experiment.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(),
        label='Experiment',
    )
    
    resource = forms.ModelMultipleChoiceField(
        queryset=Resource.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(),
        label='Resource',
    )

    units = forms.IntegerField(
        required=True,
        initial=0,
        widget=forms.NumberInput(),
        label='Resource Units',
    )

    class Meta:
        model = Resource
        fields = (
            'name',
            'description',
            'experiment',
            'resource',
            'units',
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

    resource = forms.ModelMultipleChoiceField(
        queryset=Resource.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(),
        label='Resource',
    )

    units = forms.IntegerField(
        required=True,
        initial=0,
        widget=forms.NumberInput(),
        label='Resource Units',
    )

    class Meta:
        model = Resource
        fields = (
            'name',
            'description',
            'resource',
            'units',
        )