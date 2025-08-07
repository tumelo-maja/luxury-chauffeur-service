from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('contact/', contact_form_view, name='contact'),
    path('success/', success_view, name='success'),
]
