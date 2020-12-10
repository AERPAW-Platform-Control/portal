# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import create_new_signup
from .forms import AerpawUserSignupForm

def profile(request):
    """

    :param request:
    :return:
    """
    user = request.user
    return render(request, 'profile.html', {'user': user})

def signup(request):
    """

    :param request:
    :return:
    """

    if request.method == "POST":
        form = AerpawUserSignupForm(request.POST)
        if form.is_valid():
            signup_uuid = create_new_signup(request, form)
            return redirect('home')
    else:
        form =AerpawUserSignupForm()
    return render(request, 'signup.html', {'form': form})
