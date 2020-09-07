from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

from ..forms import PartnerSignUpForm
from ..models import User

def partner_register(response):
    if response.method == "POST":
        form = PartnerSignUpForm(response.POST)
        if form.is_valid():
            new_partner = form.save()
            login(response, new_partner)
            return redirect("/")
    else:
        form = PartnerSignUpForm()

    return render(response, "businessSignUp.html", {"form":form})
