from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from register.decorators import user_required
from django.contrib import messages
import datetime
from pytz import timezone
from ..forms import AppointmentForm
from ..models import Appointment, Service
from . import manage_account
from django.urls import reverse

@login_required
@user_required
def make_appointment(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        raise Http404('service not found')

    if request.method == "POST":
        form = AppointmentForm(request.POST, service=service, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = AppointmentForm(service=service, user=request.user)
    return render(request, "schedule_appointment.html", {"form":form, 'service':service,})

@login_required
@user_required
def cancel_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        raise Http404('Appointment not found')

    if not appointment.customer.id == request.user.id:
        return redirect("/")

    if appointment.startTime.astimezone(timezone('America/Chicago')).replace(tzinfo=None) - datetime.timedelta(hours=24) < datetime.datetime.now():
        messages.error(request, "Upcoming service within 24 hours can not be cancelled.")
        return HttpResponseRedirect(reverse('customer_management'))

    elif request.method == "POST":
        appointment.status = 'CANCELLED'
        appointment.save()
        return HttpResponseRedirect(reverse('customer_management'))

    return HttpResponseRedirect(reverse('customer_management'))
