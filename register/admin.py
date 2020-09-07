from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Partner, ApiMap

admin.site.register(User, UserAdmin)
admin.site.register(Partner)
admin.site.register(ApiMap)
