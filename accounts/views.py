# accounts/views.py
from django.shortcuts import render


def profile(request):
    """

    :param request:
    :return:
    """
    user = request.user
    return render(request, 'profile.html', {'user': user})
