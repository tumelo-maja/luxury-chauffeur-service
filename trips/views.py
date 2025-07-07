from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Trip
from .forms import *

# Create your views here.


@login_required
def trip_view(request):
    # get all trips and filter for logged in user
    # trips = Trip.objects.filter(passenger=request.user)
    trips = Trip.objects.filter(
        passenger__profile__user=request.user
    )

    context = {
        'trips': trips,
        'user': request.user
    }

    return render(request, 'trips/trip.html', context)

@login_required
def trip_detail_view(request, trip_name):

    queryset = Trip.objects.filter(trip_name=trip_name)
    trip = get_object_or_404(queryset)

    context = {
        'trip': trip,
        'user': request.user,
        }
    return render(request, 'trips/partials/trip-detail.html', context)


@login_required
def trip_request_view(request):

    if request.method == 'POST':
        form = TripRequestForm(request.POST)
        if form.is_valid():
            
            trip = form.save(commit=False)
            trip.passenger = request.user.profile.passenger_profile
            trip.save()

            messages.success(request, "Trip created successfully.")
            
            return redirect('trips')
    else:
        form = TripRequestForm()

    min_valid_time = datetime.now() + timedelta(hours=1)
    min_valid_time_str = min_valid_time.strftime('%Y-%m-%dT%H:%M')
     
    context = {
        'form': form,
        'min_valid_time_str': min_valid_time_str,
    }
    return render(request, 'trips/trip-request.html',context )