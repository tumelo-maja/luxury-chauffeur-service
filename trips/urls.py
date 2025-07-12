from django.urls import path
from .views import *

urlpatterns = [
    path('', trip_view, name="trips"),
    path('trips-list/<filter_trips>', trips_list_view, name="trips-list"),
    path('dashboard/', trips_dashboard_view, name="trips-dashboard"),
    path('edit/<trip_name>/', trip_edit_view, name="trip-edit"),
    path('delete/<trip_name>/', trip_delete_view, name="trip-delete"),
    path('request/', trip_request_view, name="trip-request"),
    path('trip/<trip_name>', trip_detail_view, name="trip-detail"),
]
