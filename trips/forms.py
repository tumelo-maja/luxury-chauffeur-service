from django.forms import ModelForm
from django import forms
from django.utils import timezone
from .models import *

RATING_LABELS = [('', '<-Select a rating->')]+RATING_OPTIONS


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
                attrs={'class': 'trip_datetime',
                       'placeholder': 'Select Date and Time', }
            ),
            'comments': forms.Textarea(attrs={
                'placeholder': 'Add special instructions...',
                'rows': 3,
                'maxlength': '500'
            }),
        }


class PassengerRatingForm(forms.ModelForm):

    passenger_rating = forms.ChoiceField(
        choices=RATING_LABELS,
        required=True,
        label='Rate your Chauffeur:'
    )

    passenger_rating_comments = forms.ChoiceField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False,
        label='Comments:'
    )

    class Meta:
        model = Trip
        fields = [
            'passenger_rating',
            'passenger_rating_comments',
        ]


class DriverRatingForm(forms.ModelForm):

    driver_rating = forms.ChoiceField(
        choices=RATING_LABELS,
        required=True,
        label='Rate your Passenger:'
    )

    driver_rating_comments = forms.ChoiceField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False,
        label='Comments:'
    )

    class Meta:
        model = Trip
        fields = [
            'driver_rating',
            'driver_rating_comments',
        ]
