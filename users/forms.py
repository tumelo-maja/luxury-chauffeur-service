from django.forms import ModelForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'email']
        fields = ['displayname', 'title', 'image','phone', 'home_address'] 

class ProfileSettingsForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model= User
        fields = ['email']
