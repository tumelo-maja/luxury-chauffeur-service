from django.contrib import admin
from .models import Profile, DriverProfile, PassengerProfile

# Register your models here.
admin.site.register(Profile)
admin.site.register(DriverProfile)
admin.site.register(PassengerProfile)