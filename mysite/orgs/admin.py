from django.contrib import admin
from .models import Client, Organization, Bill


admin.site.register(Client)
admin.site.register(Organization)
admin.site.register(Bill)
