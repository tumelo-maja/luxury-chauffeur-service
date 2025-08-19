from django.forms import ModelForm
from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import *

RATING_LABELS = [('', '<-Select a rating->')]+Trip.RATING_OPTIONS


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

    def clean_travel_datetime(self):
        """
        Validate that the travel_datetime is not from the past or within 30 minutes from current time.
        - does not clash with passenger's other trips 

        An error is raised if the condition is not met.

        Returns
        -------
        str
            The cleaned travel_datetime.
        """        
        travel_datetime = self.cleaned_data.get('travel_datetime')

        now = timezone.now()
        min_allowed_time = now + timedelta(minutes=90) # fixed 1-hour+ UK timezone

        if travel_datetime < min_allowed_time:
            raise forms.ValidationError("Travel time must be at least 30 minutes from now and not in the past.")

        return travel_datetime

class PassengerRatingForm(forms.ModelForm):

    passenger_rating = forms.ChoiceField(
        choices=RATING_LABELS,
        required=True,
        label='Rate your Chauffeur:'
    )

    passenger_rating_comments = forms.CharField(
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

    driver_rating_comments = forms.CharField(
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
