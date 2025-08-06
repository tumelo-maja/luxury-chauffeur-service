from django.urls import path
from .views import *


urlpatterns = [
    path('@<username>/', profile_view, name='profile'),
    path('signup/', signup_type, name='signup_type'),
    path('signup/driver/', driver_signup, name='driver_signup'),
    path('signup/passenger/', passenger_signup, name='passenger_signup'),
    path('edit/', profile_edit_view, name='profile-edit'),
    path('onboarding/', profile_edit_view, name='profile-onboarding'),
    path('settings/', profile_settings_view, name='profile-settings'),
    path('settingschange/', profile_settings_partial_view, name='profile-settingschange'),
    path('emailverify/', profile_emailverify, name='profile-emailverify'),
    path('delete/', profile_delete_view, name='profile-delete'),
]
