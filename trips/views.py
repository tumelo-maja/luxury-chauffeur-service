from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime, timedelta
from .models import Trip
from .forms import *

# Create your views here.


@login_required
def trip_view(request):
    return render(request, 'trips/trip.html')


@login_required
def trips_dashboard_view(request):
    return render(request, 'trips/trips-dashboard.html')


@login_required
def dash_details_view(request, partial):
    return render(request, f'trips/partials/dash-{partial}.html')


@login_required
def trips_dashboard_stats_view(request):

    context = {
        'stats': {
            'cancelled': Trip.objects.filter(status='cancelled').count(),
            'completed': Trip.objects.filter(status='completed').count(),
            'pending': Trip.objects.filter(status='pending').count(),
            'modified': Trip.objects.filter(status='modified').count(),
        },
    }

    return render(request, 'trips/partials/dash-trips-summary.html', context)


@login_required
def trips_list_view(request, filter_trips='all'):

    if filter_trips == "recent":
        trips = Trip.objects.filter(
            passenger__profile__user=request.user,
        ).order_by('-updated_on')[:4]

        context = {
            'trips': trips,
            'user': request.user,
        }

        return render(request, 'trips/partials/dash-table.html', context)

    else:

        trips = Trip.objects.filter(
            passenger__profile__user=request.user,
        )

        context = {
            'trips': trips,
            'user': request.user
        }

        return render(request, 'trips/trips-list.html', context)


@login_required
def trip_detail_view(request, trip_name):

    queryset = Trip.objects.filter(trip_name=trip_name)
    trip = get_object_or_404(queryset)

    is_modal = request.GET.get('modal', 'true') == 'true'

    context = {
        'trip': trip,
        'user': request.user,
        'is_modal': is_modal,
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

    # chek if trip allows edits 
    check_action_allowed(trip)

    if request.method == 'POST':
        form = TripRequestForm(request.POST, instance=trip)
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

    # chek if trip allows delete 
    check_action_allowed(trip)

    if request.method == 'POST':
        form = TripRequestForm(instance=trip)
        trip = form.save(commit=False)
        trip.status = "cancelled"
        trip.passenger = request.user.profile.passenger_profile
        trip.save()

        return HttpResponse(status=204, headers={'HX-trigger': 'tripListChanged'})

    context = {
        'trip': trip,
        'user': request.user
    }

    return render(request, 'trips/trip-delete.html', context)

def check_action_allowed(trip):

    if trip.status in ['completed', 'canceled']:
        # chek if trip allows edits 
        return HttpResponseForbidden("You cannot edit or cancel a trip that is completed or canceled.")
    