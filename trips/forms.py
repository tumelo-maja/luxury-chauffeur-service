from django.forms import ModelForm
from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import *

RATING_LABELS = [('', '<-Select a rating->')]+Trip.RATING_CHOICES


class TripRequestForm(ModelForm):
    """
    Form for passengers to make a trip request.

    Provides fields for pickup and destination locations,
    travel date/time, driver assignment, vehicle selection,
    trip type, and optional comments.
    Includes validation to prevent scheduling trips in the past or too soon.

    Fields
    ------
    location_start : str
        Pickup location for the trip.
    location_end : str
        Destination location for the trip.
    travel_datetime : datetime
        Date and time when the trip is scheduled to start.
    driver : DriverProfile
        Assigned driver for the trip.
    vehicle : str
        Selected vehicle for the trip.
    trip_type : str
        Type of trip.
    comments : str, optional
        Any additional instructions or notes for the trip.
    """

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
        Validate that the travel_datetime is not
            from the past or within 30 minutes from current time.

        An error is raised if the condition is not met.

        Returns
        -------
        str
            The cleaned travel_datetime.
        """
        travel_datetime = self.cleaned_data.get('travel_datetime')

        now = timezone.now()
        min_allowed_time = now + timedelta(minutes=30)

        if travel_datetime < min_allowed_time:
            raise forms.ValidationError(
                "Travel time must be at least" +
                 " 30 minutes from now and not in the past.")

        return travel_datetime


class PassengerRatingForm(forms.ModelForm):
    """
    Form for passengers to rate a completed trip.

    Fields
    ------
    passenger_rating : int
        Rating for the driver/trip experience (1-5 stars).
    passenger_rating_comments : str, optional
        Optional comments about the trip.
    """
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
    """
    Form for driver to rate a completed trip.

    Fields
    ------
    driver_rating : int
        Rating for the passenger (1-5 stars).
    driver_rating_comments : str, optional
        Optional comments about the trip.
    """
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
