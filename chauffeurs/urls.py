from django.urls import path 
from .views import *

urlpatterns = [
    path('',chauffeurs_view, name="chauffeurs"),
]