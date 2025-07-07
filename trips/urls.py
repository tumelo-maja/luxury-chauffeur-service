from django.urls import path
from .views import *

urlpatterns = [
    path('', trip_view, name="trips"),
    path('request', trip_request_view, name="trip-request"),
    path('trip/<trip_name>', trip_detail_view, name="trip-detail"),
]
