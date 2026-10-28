from django.contrib import admin
from .models import UserRegistrations,HOSPITALRegistrations,Donations,OrganRequest

admin.site.register(UserRegistrations)
admin.site.register(HOSPITALRegistrations)
admin.site.register(Donations)
admin.site.register(OrganRequest)
