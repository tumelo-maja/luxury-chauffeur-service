from django.forms import ModelForm
from django import forms
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'email']
        fields = ['displayname', 'title', 'phone', 'home_address'] 


