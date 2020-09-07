from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect("/") 