from django.urls import path
from .views import *

urlpatterns = [
    path('', trip_view, name="trips"),
    path('trips-list/', trips_list_view, name="trips-list"),
    path('edit/<trip_name>/', trip_edit_view, name="trip-edit"),
    path('request/', trip_request_view, name="trip-request"),
    path('trip/<trip_name>', trip_detail_view, name="trip-detail"),
]
