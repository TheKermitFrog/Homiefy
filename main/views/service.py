from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from register.decorators import partner_required
from register.models import Partner, User, ApiMap
from yelpreview.models import yelpReview
from ..forms import ServiceForm, UpdateServiceForm
from ..models import Service
from django.http import Http404

@login_required
@partner_required
def create_service(response):
    if response.method == "POST":
        form = ServiceForm(response.POST, user=response.user)
        if form.is_valid():
            form.save()
            return redirect("partner_management")
    else:
        form = ServiceForm()

    return render(response, "create_service.html", {"form":form})

def service_info(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        raise Http404('Service not found')

    # get according reviews
    try:
        map = ApiMap.objects.get(businessPartner = service.businessPartner)
    except ApiMap.DoesNotExist:
        map = None
    if map:
        reviews = yelpReview.objects.filter(yelpBusinessId = map).filter(tag__icontains = service.type)
    else:
        reviews = None
    return render(request, 'service.html', {
        'service' : service, 'reviews' : reviews
    })

@login_required
@partner_required
def update_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        raise Http404('service not found')

    if not service.businessPartner == Partner.objects.get(user = request.user):
        return redirect("/")
    if request.method == "POST":

        form = UpdateServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect("partner_management")
    else:
        form = UpdateServiceForm(instance=service)
    return render(request, 'update_service.html', {'form': form, 'service':service})

@login_required
@partner_required
def delete_service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        raise Http404('service not found')

    if not service.businessPartner == Partner.objects.get(user = request.user):
        return redirect("/")
    if request.method == "POST":
        service.delete()
        return redirect('partner_management')
    return redirect('partner_management')
