from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import Trip
from .forms import *

# Create your views here.


@login_required
def trip_view(request):
    return render(request, 'trips/trip.html')


@login_required
def trips_list_view(request):
    trips = Trip.objects.filter(
        passenger__profile__user=request.user,
    ).exclude(status='cancelled')

    context = {
        'trips': trips,
        'user': request.user
    }

    return render(request, 'trips/trips-list.html', context)


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

            # messages.success(request, "Trip created successfully.")
            # return redirect('trips')

            return HttpResponse(status=204, headers={'HX-trigger': 'tripListChanged'})

    else:
        form = TripRequestForm()

    min_valid_time = datetime.now() + timedelta(hours=1)
    min_valid_time_str = min_valid_time.strftime('%Y-%m-%dT%H:%M')

    context = {
        'form': form,
        'min_valid_time_str': min_valid_time_str,
    }
    return render(request, 'trips/trip-request.html', context)


@login_required
def trip_edit_view(request, trip_name):

    # queryset = Trip.objects.filter(trip_name=trip_name)
    # trip = get_object_or_404(queryset)
    trip = get_object_or_404(Trip, trip_name=trip_name)
    # form = TripRequestForm(instance=trip)

    if request.method == 'POST':
        form = TripRequestForm(request.POST)
        if form.is_valid():

            trip = form.save(commit=False)
            trip.status = "modified"
            trip.passenger = request.user.profile.passenger_profile
            trip.save()

            # messages.success(request, "Changes saved successfully.")

            return HttpResponse(status=204, headers={'HX-trigger': 'tripListChanged'})

    else:
        form = TripRequestForm(instance=trip)

    context = {
        'trip': trip,
        'form': form,
        'user': request.user,
    }

    return render(request, 'trips/trip-edit.html', context)


@login_required
def trip_delete_view(request, trip_name):

    trip = get_object_or_404(Trip, trip_name=trip_name)

    if request.method == 'POST':
        form = TripRequestForm(instance=trip)
        print("Foooooorm")
        trip = form.save(commit=False)
        trip.status = "cancelled"
        trip.passenger = request.user.profile.passenger_profile
        trip.save()
        print("stoooooooooooooooooooooooop")

        return HttpResponse(status=204, headers={'HX-trigger': 'tripListChanged'})

    context = {
        'trip': trip,
        'user': request.user
    }

    return render(request, 'trips/trip-delete.html', context)
