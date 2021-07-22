from django import forms

from accounts.models import AerpawUser
from projects.models import Project
from .models import Profile


class ProfileCreateForm(forms.ModelForm):

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True,
        widget=forms.Select(),
        label='Project',
    )

    profile = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Definition',
    )

    class Meta:
        model = Profile
        fields = (
            'name',
            'description',
            'project',
            'profile',
            #'created_by',
            #'created_date',
            #'stage',
        )

    def clean_title(self):
        data = self.cleaned_data.get('name')
        if len(data) <4:
            raise forms.ValidationError("The name is not long enough!")
        return data

class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Description',
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.order_by('name'),
        required=True,
        initial=0,
        widget=forms.Select(),
        label='Project',
    )

    profile = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Definition',
    )

    class Meta:
        model = Profile
        fields = (
            'name',
            'description',
            'project',
            'profile',
            #'modified_by',
            #'modified_date',
            #'stage',
        )