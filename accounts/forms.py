# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AerpawUser, AerpawUserSignup, AerpawUserCredential, AerpawRoleRequest, AerpawUserRoleChoice


class AerpawUserCreationForm(UserCreationForm):
    class Meta:
        model = AerpawUser
        fields = ('username', 'email', 'first_name', 'last_name', 'oidc_claim_sub')


class AerpawUserChangeForm(UserChangeForm):
    class Meta:
        model = AerpawUser
        fields = ('username', 'email', 'first_name', 'last_name', 'oidc_claim_sub')


class AerpawUserSignupForm(forms.ModelForm):
    class Meta:
        model = AerpawUserSignup
        fields = ('user', 'name', 'title', 'organization', 'description', 'userRole', 'publickey')


class AerpawUserCredentialForm(forms.ModelForm):
    class Meta:
        model = AerpawUserCredential
        fields = ('publickey',)


class AerpawRoleRequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AerpawRoleRequestForm, self).__init__(*args, **kwargs)
        self.fields['purpose'].label = "Reason for request?"
        all_choices = AerpawUserRoleChoice.choices()
        cur_roles = self.user.groups.all()
        cur_role_list = []
        for role in cur_roles:
            cur_role_list.append(str(role))
        display_choices = [('', '--------')]
        for ch in all_choices:
            if str(ch[0]) not in cur_role_list:
                display_choices.append(ch)
        self.fields['requested_role'].choices = display_choices

    class Meta:
        model = AerpawRoleRequest
        fields = (
            'requested_role',
            'purpose'
        )

    requested_role = forms.ChoiceField(
        widget=forms.Select,
        label='Role Function'
    )
