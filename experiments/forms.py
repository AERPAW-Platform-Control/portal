from django import forms

from accounts.models import AerpawUser
from projects.models import Project
from reservations.models import Reservation
from profiles.models import Profile
from .models import Experiment


class ExperimentCreateForm(forms.ModelForm):
    experimenter = forms.ModelMultipleChoiceField(
        queryset=AerpawUser.objects.order_by('oidc_claim_name'),
        required=True,
        widget=forms.SelectMultiple(),
        label='Lead Experimenter',
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.none(),
        required=True,
        widget=forms.Select(),
        label='Project',
    )

    profile = forms.ModelChoiceField(
        queryset=Profile.objects.order_by('name'),
        required=False,
        widget=forms.Select(),
        label='Profile',
    )

    class Meta:
        model = Experiment
        fields = (
            'name',
            'description',
            'experimenter',
            'project',
            'stage',
        )

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        experimenter = kwargs.pop('experimenter', None)
        super().__init__(*args, **kwargs)
        if project and experimenter:
            qs = Project.objects.filter(project_members__id=experimenter.id)
            if qs:
                self.fields['project'].queryset = qs

            qs = AerpawUser.objects.filter(projects__id=project.id)
            print(qs)
            if qs:
                self.fields['experimenter'].queryset = qs

    def clean_title(self):
        data = self.cleaned_data.get('name')
        if len(data) <4:
            raise forms.ValidationError("The name is not long enough!")
        return data

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
        label='Lead Experimenter',
    )

    experiment_reservations = forms.ModelMultipleChoiceField(
        queryset=Reservation.objects.order_by('name'),
        required=False,
        widget=forms.SelectMultiple(),
        label='Experiment Reservations',
    )

    profile = forms.ModelChoiceField(
        queryset=Profile.objects.order_by('name'),
        required=False,
        widget=forms.Select(),
        label='Profile',
    )

    class Meta:
        model = Experiment
        fields = (
            'name',
            'description',
            'experimenter',
            'modified_by',
            'modified_date',
            'stage',
        )
