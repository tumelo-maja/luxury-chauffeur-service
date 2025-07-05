from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'email']
        fields = ['displayname', 'title', 'image','phone', 'home_address'] 


class PassengerProfileForm(ModelForm):
    class Meta:
        model = PassengerProfile
        fields = ['emergency_name', 'emergency_phone']


class DriverProfileForm(ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['experience'] 


class ProfileSettingsForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model= User
        fields = ['email']
