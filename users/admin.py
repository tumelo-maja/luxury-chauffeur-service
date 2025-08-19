from django.contrib import admin
from .models import Profile, DriverProfile, PassengerProfile, ManagerProfile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone')
    list_filter = ('user_type',)

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('profile','status',)
    search_fields = ('profile__user__username',)
admin.site.register(PassengerProfile, PassengerAdmin)

class DriverAdmin(admin.ModelAdmin):
    list_display = ('profile','status',)
    search_fields = ('profile__user__username',)
admin.site.register(DriverProfile, DriverAdmin)

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('profile','status',)
    search_fields = ('profile__user__username',)
admin.site.register(ManagerProfile, ManagerAdmin)

