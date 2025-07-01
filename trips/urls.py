from django.urls import path 
from .views import *

urlpatterns = [
    path('',trip_view, name="trips"),
]