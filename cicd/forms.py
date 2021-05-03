from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDict
from accounts.models import AerpawUser
from .models import Cicd, CicdHostInfo

"""
aerpaw_uuid - from project uuid
fqdn_or_ip - from admin settings
jenkins_admin_id - from pi
jenkins_admin_password - from pi
jenkins_admin_name - from pi
jenkins_service_agent_port - from resource allocation
jenkins_ssh_agent_port - from resource allocation
fqdn_or_ip - fully qualified domain name or IP address
nginx_http_port - from resource allocation
nginx_https_port - from resource allocation
"""

class CicdCreateHostInfoForm(forms.ModelForm):

    # def __init__(self, data, **kwargs):
    #     initial = kwargs.get("initial", {})
    #     data = MultiValueDict({**{k: [v] for k, v in initial.items()}, **data})
    #     super().__init__(data, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='CI/CD Name',
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        required=False,
        label='CI/CD Description',
    )
    fqdn_or_ip = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='FQDN or IP',
    )
    docker_subnet = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Docker Subnet',
    )
    jenkins_service_agent_port = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Jenkins Agent Port',
    )
    jenkins_ssh_agent_port = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Jenkins SSH Port',
    )
    gitea_ssh_agent_port = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Gitea SSH Port',
    )
    nginx_http_port = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='HTTP Port',
    )
    nginx_https_port = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='HTTPS Port',
    )

    class Meta:
        model = CicdHostInfo
        fields = (
            'name',
            'description',
            'fqdn_or_ip',
            'docker_subnet',
            'jenkins_service_agent_port',
            'jenkins_ssh_agent_port',
            'gitea_ssh_agent_port',
            'nginx_http_port',
            'nginx_https_port',
        )


class CicdCreateForm(forms.ModelForm):

    def __init__(self, data, **kwargs):
        initial = kwargs.get("initial", {})
        data = MultiValueDict({**{k: [v] for k, v in initial.items()}, **data})
        super().__init__(data, **kwargs)

    cicd_host = forms.ModelChoiceField(
        queryset=CicdHostInfo.objects.filter(is_allocated=False).order_by('name'),
        required=True,
        initial=0,
        widget=forms.Select(),
        label='CI/CD Host',
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='CI/CD Name',
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        required=False,
        label='CI/CD Description',
    )
    # fqdn_or_ip = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='FQDN or IP',
    #     disabled=True,
    # )
    # docker_subnet = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='Docker Subnet',
    #     disabled=True,
    # )
    # jenkins_admin_name = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='Jenkins Admin Name',
    # )
    jenkins_admin_password = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Jenkins Admin Password',
    )
    # jenkins_service_agent_port = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='Jenkins Agent Port',
    #     disabled=True,
    # )
    # jenkins_ssh_agent_port = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='Jenkins SSH Port',
    #     disabled=True,
    # )
    # nginx_http_port = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='HTTP Port',
    #     disabled=True,
    # )
    # nginx_https_port = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='HTTPS Port',
    #     disabled=True,
    # )
    aerpaw_uuid = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=False,
        label='AERPAW Project UUID',
        disabled=True,
    )

    class Meta:
        model = Cicd
        fields = (
            'name',
            'description',
            'jenkins_admin_password',
            'aerpaw_uuid',
        )


class CicdUpdateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='CI/CD Name',
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        required=False,
        label='CI/CD Description',
    )
    # fqdn_or_ip = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='FQDN or IP',
    # )
    # jenkins_admin_name = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='Jenkins Admin Name',
    # )
    # jenkins_admin_password = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='Jenkins Admin Password',
    # )
    # jenkins_service_agent_port = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='Jenkins Agent Port',
    # )
    # jenkins_ssh_agent_port = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='Jenkins SSH Port',
    # )
    # nginx_http_port = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='HTTP Port',
    # )
    # nginx_https_port = forms.CharField(
    #     widget=forms.TextInput(attrs={'size': 60}),
    #     required=True,
    #     label='HTTPS Port',
    # )
    aerpaw_uuid = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=False,
        label='AERPAW Project UUID',
        disabled=True,
    )

    class Meta:
        model = Cicd
        fields = (
            'name',
            'description',
            # 'fqdn_or_ip',
            # 'jenkins_admin_name',
            # 'jenkins_admin_password',
            # 'jenkins_service_agent_port',
            # 'jenkins_ssh_agent_port',
            # 'nginx_http_port',
            # 'nginx_https_port',
            'aerpaw_uuid',
        )
