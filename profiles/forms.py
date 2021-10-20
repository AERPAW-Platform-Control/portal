from django import forms

from projects.models import Project
from .models import Profile


class ProfileCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.pr = kwargs.pop('project', None)
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        self.projects = Project.objects.filter(id=self.pr.id)

        self.fields['project'] = forms.ModelChoiceField(
            queryset=self.projects,
            initial=self.pr,
            required=True,
            widget=forms.Select(),
            label='Project'
        )

    class Meta:
        model = Profile
        fields = (
            'name',
            'description',
            'project',
            'profile',
            # 'created_by',
            # 'created_date',
            # 'stage',
        )

    profile = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Definition',
    )

    def clean_title(self):
        data = self.cleaned_data.get('name')
        if len(data) < 4:
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
            # 'modified_by',
            # 'modified_date',
            # 'stage',
        )
