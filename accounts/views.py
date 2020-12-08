# accounts/views.py
from django.shortcuts import render
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
            return redirect('signup')
    else:
        form =AerpawUserSignupForm()
    return render(request, 'signup.html', {'form': form})
