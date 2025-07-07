from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .models import *


class TripRequestForm(ModelForm):

    class Meta:
        model = Trip
        fields = [
            'location_start',
            'location_end',
            'travel_datetime',
            'driver',
            'vehicle',
            'trip_type',
            'comments',
        ]

        widgets = {
            'location_start': forms.TextInput(attrs={
                'placeholder': 'Enter pickup location...',
                'autofocus': True
            }),
            'location_end': forms.TextInput(attrs={
                'placeholder': 'Enter destination...',
            }),
            'travel_datetime': forms.DateTimeInput(
                attrs={'id': 'trip_datetime', 'placeholder': 'Select Date and Time',}
            ),
            'comments': forms.Textarea(attrs={
                'placeholder': 'Add special instructions...',
                'rows': 3,
                'maxlength': '500'
            }),
        }
