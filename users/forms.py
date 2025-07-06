from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['title', 'displayname', 'image', 'phone', 'home_address']


class MainSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['title', 'displayname', 'image', 'phone', 'home_address']


class DriverEditForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['experience']
        labels = {'experience': 'Years of driving experience'}


class PassengerEditForm(forms.ModelForm):
    class Meta:
        model = PassengerProfile
        fields = ['emergency_name', 'emergency_phone']


class ProfileSettingsForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']
