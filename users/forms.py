from django.forms import ModelForm
from django import forms
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = ['preferred_name', 'title', 'email', 'phone', 'home_address'] 


