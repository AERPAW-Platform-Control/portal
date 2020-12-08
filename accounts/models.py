# accounts/models.py
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Extends basic User model: https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
class AerpawUser(AbstractUser):
    # universal unique identifier for user within infrastructure
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    # oidc scope openid
    oidc_claim_sub = models.CharField(max_length=255)
    oidc_claim_iss = models.CharField(max_length=255)
    oidc_claim_aud = models.CharField(max_length=255)
    oidc_claim_token_id = models.CharField(max_length=255)

    # oidc scope email
    oidc_claim_email = models.CharField(max_length=255)

    # oidc scope profile
    oidc_claim_given_name = models.CharField(max_length=255)
    oidc_claim_family_name = models.CharField(max_length=255)
    oidc_claim_name = models.CharField(max_length=255)

    # oidc scope org.cilogon.userinfo
    oidc_claim_idp = models.CharField(max_length=255)
    oidc_claim_idp_name = models.CharField(max_length=255)
    oidc_claim_eppn = models.CharField(max_length=255)
    oidc_claim_eptid = models.CharField(max_length=255)
    oidc_claim_affiliation = models.CharField(max_length=255)
    oidc_claim_ou = models.CharField(max_length=255)
    oidc_claim_oidc = models.CharField(max_length=255)
    oidc_claim_cert_subject_dn = models.CharField(max_length=255)

    # oidc other values
    oidc_claim_acr = models.CharField(max_length=255)
    oidc_claim_entitlement = models.CharField(max_length=255)

    def __str__(self):
        return self.oidc_claim_name + ' (' + self.username + ')'

def is_PI(user):
    print(user)
    print(user.groups.all())
    return user.groups.filter(name='PI').exists()

def is_project_member(user,project_group):
    print(user)
    print(user.groups.all())
    return user.groups.filter(name=project_group).exists()