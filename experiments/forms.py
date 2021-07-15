from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.widgets import FilteredSelectMultiple

from accounts.models import AerpawUser
from projects.models import Project
from reservations.models import Reservation
from profiles.models import Profile
from .models import Experiment, UserStageChoice, StageChoice


class ExperimentCreateForm(forms.ModelForm):
    profile = forms.ModelChoiceField(
        queryset=Profile.objects.order_by('name'),
        required=True,
        widget=forms.Select(),
        label='Experiment Definition',
    )

    class Meta:
        model = Experiment
        fields = [
            'name',
            'description',
            'profile'
        ]


class ExperimentUpdateExperimentersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # self.experimenter = kwargs.pop('experimenter')
        super(ExperimentUpdateExperimentersForm, self).__init__(*args, **kwargs)
        exp = kwargs.get('instance')
        project = Project.objects.get(id=int(exp.project_id))
        self.fields['experimenter'].queryset = (project.project_owners.all() | project.project_members.all()).distinct()

    class Media:
        extend = False
        css = {
            'all': [
                'admin/css/widgets.css'
            ]
        }
        js = (
            'js/django_global.js',
            'admin/js/jquery.init.js',
            'admin/js/core.js',
            'admin/js/prepopulate_init.js',
            'admin/js/prepopulate.js',
            'admin/js/SelectBox.js',
            'admin/js/SelectFilter2.js',
            'admin/js/admin/RelatedObjectLookups.js',
        )

    class Meta:
        model = Experiment
        fields = [
            'experimenter'
        ]

    experimenter = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=FilteredSelectMultiple("Experimenters", is_stacked=False),
        required=False
    )


# class ExperimentCreateForm(forms.ModelForm):
#     experimenter = forms.ModelChoiceField(
#         queryset=AerpawUser.objects.order_by('oidc_claim_name'),
#         required=True,
#         widget=forms.Select(),
#         label='Lead Experimenter',
#     )
#
#     project = forms.ModelChoiceField(
#         queryset=Project.objects.none(),
#         required=True,
#         widget=forms.Select(),
#         label='Project',
#     )
#
#     stage = forms.ChoiceField(
#         choices=ResourceStageRequestChoice.choices(),
#         required=True,
#         widget=forms.Select(),
#         label='Stage',
#     )
#
#     profile = forms.ModelChoiceField(
#         queryset=Profile.objects.order_by('name'),
#         required=False,
#         widget=forms.Select(),
#         label='Profile',
#     )
#
#     class Meta:
#         model = Experiment
#         fields = (
#             'name',
#             'description',
#             'experimenter',
#             'project',
#             'stage',
#         )
#
#     def __init__(self, *args, **kwargs):
#         project = kwargs.pop('project', None)
#         experimenter = kwargs.pop('experimenter', None)
#         super().__init__(*args, **kwargs)
#         if project and experimenter:
#             qs = Project.objects.filter(project_members__id=experimenter.id)
#             if qs:
#                 self.fields['project'].queryset = qs
#
#             qs = AerpawUser.objects.filter(projects__id=project.id)
#             #print(qs)
#             if qs:
#                 self.fields['experimenter'].queryset = qs
#
#     def clean_title(self):
#         data = self.cleaned_data.get('name')
#         if len(data) <4:
#             raise forms.ValidationError("The name is not long enough!")
#         return data
#
#     def clean(self, *args, **kwargs):
#         cleaned_data = super().clean(*args, **kwargs)
#
#         rs=cleaned_data.get("name")
#         qs=Experiment.objects.filter(name=rs)
#         if qs.exists():
#             raise forms.ValidationError("This experiment name has been used!")
#             return redirect("/create")
#
#         return cleaned_data


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

    '''
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

    stage = forms.ChoiceField(
        choices=UserStageChoice.choices(),
        required=True,
        widget=forms.Select(),
        label='Stage',
    )

    profile = forms.ModelChoiceField(
        queryset=Profile.objects.order_by('name'),
        required=False,
        widget=forms.Select(),
        label='Experiment Definition',
    )
    '''

    class Meta:
        model = Experiment
        fields = (
            'name',
            'description',
        )


class ExperimentUpdateByOpsForm(forms.ModelForm):

    stage = forms.ChoiceField(
        choices=StageChoice.choices(),
        required=True,
        widget=forms.Select(),
        label='Mode',
    )

    state = forms.ChoiceField(
        choices=Experiment.STATE_CHOICES,
        required=True,
        widget=forms.Select(),
        label='state',
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Experiment Notification',
    )

    class Meta:
        model = Experiment
        fields = (
            'stage',
            'state',
            'message',
        )


class ExperimentSubmitForm(forms.ModelForm):
    stage = forms.ChoiceField(
        choices=UserStageChoice.choices(),
        required=True,
        widget=forms.Select(),
        label='Submit to',
    )

    class Meta:
        model = Experiment
        fields = (
            'stage',
        )


class ExperimentAdminForm(forms.ModelForm):
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

    stage = forms.ChoiceField(
        choices=StageChoice.choices(),
        required=True,
        widget=forms.Select(),
        label='Stage',
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
            'profile',
        )
