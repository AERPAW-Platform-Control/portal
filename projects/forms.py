from django import forms

from accounts.models import AerpawUser
from .models import Project


class ProjectCreateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Project Name',
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        required=False,
        label='Project Description',
    )

    principal_investigator = forms.ModelChoiceField(
        queryset=AerpawUser.objects.order_by('oidc_claim_name'),
        required=True,
        initial=0,
        widget=forms.Select(),
        label='Principal Investigator',
    )

    # project_members = forms.ModelMultipleChoiceField(
    #     queryset=AerpawUser.objects.order_by('oidc_claim_name'),
    #     required=False,
    #     widget=forms.SelectMultiple(),
    #     label='Project Members',
    # )

    add_project_members = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        required=False,
        label='Add project members emails',
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            #'principal_investigator',
            #'project_members',
        )


class ProjectUpdateForm(forms.ModelForm):
    # name = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    # )

    # description = forms.CharField(
    #     widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
    #     required=False,
    #     label='Project Description',
    # )

    # principal_investigator = forms.ModelChoiceField(
    #     queryset=AerpawUser.objects.order_by('oidc_claim_name'),
    #     required=True,
    #     initial=0,
    #     widget=forms.Select(),
    #     label='Principal Investigator',
    # )
    delete_project_members = forms.ModelMultipleChoiceField(
        queryset=AerpawUser.objects.none(),
        required=False,
        widget=forms.SelectMultiple(),
        label='Delete Project Members',
    )

    add_project_members = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        required=False,
        label='Add project members emails',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project = self.instance
        if project:
            qs = AerpawUser.objects.filter(projects=project).order_by('oidc_claim_name')
            if qs:
                self.fields['delete_project_members'].queryset = qs

    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            #'principal_investigator',
            #'project_members',
        )
