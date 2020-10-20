from django import forms

from accounts.models import AerpawUser
from projects.models import Project
from reservations.models import Reservation
from .models import Experiment


class ExperimentCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Experiment Name',
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Experiment Description',
    )

    state = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Experiment State',
    )

    experimenter = forms.ModelChoiceField(
        queryset=AerpawUser.objects.order_by('oidc_claim_name'),
        required=True,
        initial=0,
        widget=forms.Select(),
        label='Experimenter',
    )

    experiment_reservations = forms.ModelMultipleChoiceField(
        queryset=Reservation.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(),
        label='Experiment Reservations',
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'experimenter',
            'experiment_reservations',
        )


class ExperimentUpdateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Experiment Description',
    )

    experimenter = forms.ModelChoiceField(
        queryset=AerpawUser.objects.order_by('oidc_claim_name'),
        required=True,
        initial=0,
        widget=forms.Select(),
        label='Experimenter',
    )

    experiment_reservations = forms.ModelMultipleChoiceField(
        queryset=Reservation.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(),
        label='Experiment Reservations',
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'experimenter',
            'experiment_reservations',
        )