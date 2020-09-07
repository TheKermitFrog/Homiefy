"""house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from register.views import user, partner, logout
from main.views import home, appointment, service, manage_account, search
from service_categories.views import service_categories


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.home),
    path('services', home.services),
    path('about', home.about),
    path('user_register', user.user_register, name="user_register"),
    path('partner_register', partner.partner_register, name="partner_register"),
    path('accounts/logout', logout.logout_view, name='logout'),
    path('partner_register', partner.partner_register, name="partner_register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('create_service', service.create_service, name="create_service"),
    path('service/<int:service_id>/', service.service_info, name="service_info"),
    path('service/<int:service_id>/appointment', appointment.make_appointment, name="make_appointment"),
    path('service/<int:service_id>/update', service.update_service, name="update_service"),
    path('service/<int:service_id>/delete', service.delete_service, name="delete_service"),
    path('service/type/<type>', service_categories.service_categories, name="service_categories"),
    path('search/', search.search_result_view, name='search_result'),
    path('partner_management', manage_account.partner_management, name="partner_management"),
    path('customer_management', manage_account.customer_management, name="customer_management"),
    path('appointment/<int:appointment_id>/cancel', appointment.cancel_appointment, name="cancel_appointment"),
]
