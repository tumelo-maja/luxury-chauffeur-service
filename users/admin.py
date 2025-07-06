from django.contrib import admin
from .models import Profile, DriverProfile, PassengerProfile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone')
    list_filter = ('user_type',)
admin.site.register(DriverProfile)
admin.site.register(PassengerProfile)
