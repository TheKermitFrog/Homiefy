from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from register.decorators import partner_required, user_required
from register.models import Partner, User
from ..models import Service, Appointment
from django.http import Http404
import datetime
from pytz import timezone
from django.db.models import Q

@login_required
@partner_required
def partner_management(request):
    current_partner = Partner.objects.get(user = request.user)
    # list upcoming Appointment
    upcoming_appointment = Appointment.objects.filter(partner = current_partner)
    upcoming_appointment = upcoming_appointment.filter(startTime__gte=datetime.datetime.now().astimezone(timezone('utc')))
    upcoming_appointment = upcoming_appointment.filter(status = 'Booked')
    # list available service
    available_service = Service.objects.filter(businessPartner = current_partner)
    return render(request, 'partner_info.html', {'appointments' : upcoming_appointment, 'services' : available_service})

@login_required
@user_required
def customer_management(request):
    current_customer = User.objects.get(id = request.user.id)
    # list upcoming Appointment
    appointments = Appointment.objects.filter(customer = current_customer)
    upcoming_appointment = appointments.filter(startTime__gte=datetime.datetime.now().astimezone(timezone('utc')))
    upcoming_appointment = upcoming_appointment.filter(status = 'BOOKED')
    # list cancelled and past Appointment
    past_appointment = appointments.filter(Q(endTime__lt=datetime.datetime.now().astimezone(timezone('utc'))) | Q(status = 'Cancelled'))
    return render(request, 'customer_profile.html', {'upcoming_appointments' : upcoming_appointment, 'past_appointments': past_appointment})
