from django.contrib import admin
from .models import Trip

# Register your models here.
class TripAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'driver','location_end','status','travel_datetime', 'updated_on','created_on','trip_name')
    list_filter = ('passenger', 'driver','status',)

admin.site.register(Trip,TripAdmin)
