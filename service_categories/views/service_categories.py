from django.shortcuts import render, redirect
from main.models import Service, Appointment
from django.db.models import Count
from django.db.models.functions import Lower
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def service_categories(request, type):
    service_type = Service.objects.values_list(Lower('type'), flat = True).distinct()

    if type not in service_type:
        raise Http404('Unknown service type: ' + type)
    # A list of services under the given type
    services = Service.objects.filter(type=type)

    paginator = Paginator(services, 5)
    page = request.GET.get('page', 1)

    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        services = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        services = paginator.page(paginator.num_pages)

    # Get top 3 popular services under that service_categories
    # top popular -> service with the highest amount of completed appointment
    Apps = Appointment.objects.filter(service__type=type).values('service').annotate(count=Count('service')).order_by('count')[:3]

    top3_service = []
    for app in Apps:
        top3_service.append([Service.objects.get(id = app['service']), app['count']])

    return render(request, 'serv_categories.html', {'services':services, 'top3': top3_service, 'type': type, 'service_types':service_type})
