from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.shortcuts import render

from register.models import User, Partner
from main.models import Service, Appointment

def search_result_view(request):
    service_queryset = Service.objects.all() \
                        .values('id', 'businessPartner__businessName', 'type', 'businessPartner__description', 'maxCapacity', 'price', 'duration')
    # bp_queryset = Partner.object.all()

    query = request.GET.get("q")
    if query:
        service_queryset = service_queryset.filter(
                                        Q(businessPartner__businessType__icontains=query) |
                                        Q(businessPartner__businessName__icontains=query) |
                                        Q(businessPartner__description__icontains=query)
                                        )

    paginator = Paginator(service_queryset, 10)
    page = request.GET.get('page', 1)

    try:
        service_queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        service_queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        service_queryset = paginator.page(paginator.num_pages)

    # return the most popular services when no keyword matching
    Apps = Appointment.objects.all().values('service').annotate(count=Count('service')).order_by('count')[:10]

    popular_services = []
    for app in Apps:
        popular_services.append(Service.objects.get(id = app['service']))

    context = {
        "service_list": service_queryset,
        "popular_list": popular_services
    }

    return render(request, 'search_results.html', context)
