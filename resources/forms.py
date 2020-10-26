from django import forms

from accounts.models import AerpawUser
from projects.models import Project
from reservations.models import Reservation
from .models import Resource,ResourceStageChoice,ResourceTypeChoice

class ResourceCreateForm(forms.ModelForm):
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

    resourceType = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Resource Type',
    )

    units = forms.IntegerField(
        required=True,
        initial=0,
        widget=forms.NumberInput(),
        label='Resource Units',
    )

    location = forms.ModelMultipleChoiceField(
        queryset=Reservation.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(),
        label='Resource Location',
    )

    stage = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Resource Stage',
    )

    class Meta:
        model = Resource
        fields = (
            'name',
            'description',
            'units',
            'location',
        )


class ResourceChangeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Resource Description',
    )

    resoureceType = forms.CharField(
        required=True,
        initial=0,
        widget=forms.Select(),
        label='resourceType',
    )

    location = forms.ModelMultipleChoiceField(
        queryset=Reservation.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(),
        label='Experiment Location',
    )

    class Meta:
        model = Resource
        fields = (
            'name',
            'description',
            'resourceType',
            'location',
        )
