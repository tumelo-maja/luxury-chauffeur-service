from django.contrib import admin
from .models import Profile, DriverProfile, PassengerProfile, ManagerProfile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone')
    list_filter = ('user_type',)
admin.site.register(PassengerProfile)

class DriverAdmin(admin.ModelAdmin):
    list_display = ('profile', 'status')
    list_filter = ('status',)
    search_fields = ('profile__user__username',)

admin.site.register(DriverProfile, DriverAdmin)
admin.site.register(ManagerProfile)

