from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from main.models import Service


# Create your views here.
def home(request):
    services = Service.objects.all()
    service_type = Service.objects.order_by().values('type').distinct()
    return render(request, 'index.html', {'services': services, 'types': service_type})

def services(request):
    services = Service.objects.all()
    service_type = Service.objects.order_by().values('type').distinct()
    return render(request, 'services.html',{'services': services, 'types': service_type})

def about(request):
    return render(request, 'about.html')

def signIn(request):
    return render(request, 'sign-in.html')

def customerSignUp(request):
    return render(request, 'customerSignUp.html')

def businessSignUp(request):
    return render(request, 'businessSignUp.html')
