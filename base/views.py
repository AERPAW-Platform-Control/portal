from uuid import UUID
import os
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone


def home(request):
    """

    :param request:
    :return:
    """
    if request.user.is_authenticated:
        operator_cicd = {
            'url': os.getenv('OPERATOR_CICD_URL'),
            'port': os.getenv('OPERATOR_CICD_PORT')
        }
        return render(request, 'home.html', {'operator_cicd': operator_cicd})
    else:
        return render(request, 'home.html')