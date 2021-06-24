from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from accounts.models import AerpawUser
from .models import Project


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
        ]


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'name',
            'description'
        )


class ProjectUpdateMembersForm(forms.ModelForm):
    project_members = forms.ModelMultipleChoiceField(
        queryset=AerpawUser.objects.all().exclude(username='admin'),
        widget=FilteredSelectMultiple("Members", is_stacked=False),
        required=False
    )

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
        model = Project
        fields = [
            'project_members'
        ]


class ProjectUpdateOwnersForm(forms.ModelForm):
    project_owners = forms.ModelMultipleChoiceField(
        queryset=AerpawUser.objects.all().exclude(username='admin'),
        widget=FilteredSelectMultiple("Members", is_stacked=False),
        required=False
    )

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
        model = Project
        fields = [
            'project_owners'
        ]
