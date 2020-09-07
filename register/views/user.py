from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

from ..forms import UserSignUpForm
from ..models import User

def user_register(response):
    if response.method == "POST":
        form = UserSignUpForm(response.POST)
        if form.is_valid():
            new_user = form.save()
            login(response, new_user)
            return redirect("/")
    else:
        form = UserSignUpForm()

    return render(response, "customerSignUp.html", {"form":form})
    # return render(response, "register/user_register.html", {"form":form})
