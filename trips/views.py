from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from datetime import datetime, timedelta
from .models import Trip
from users.models import PassengerProfile, DriverProfile
from .forms import *

# Create your views here.


@login_required
def trip_view(request):
    return render(request, 'trips/trip.html')


@login_required
def trips_dashboard_view(request):

    context = {
        'is_driver': True if request.user.profile.user_type == "driver" else False,
    }
    return render(request, 'trips/trips-dashboard.html', context)


@login_required
def dash_details_view(request, partial):
    return render(request, f'trips/partials/dash-{partial}.html')


@login_required
def trips_dashboard_stats_view(request):

    if request.user.profile.user_type == "passenger":
        trips = Trip.objects.filter(
                passenger=request.user.profile.passenger_profile,
            )
    elif request.user.profile.user_type == "driver":
        trips = Trip.objects.filter(
                driver=request.user.profile.driver_profile,
            )

    context = {
        'stats': {
            'cancelled': trips.filter(status='cancelled').count(),
            'completed': trips.filter(status='completed').count(),
            'pending': trips.filter(status='pending').count(),
            'modified': trips.filter(status='modified').count(),
        },
    }

    return render(request, 'trips/partials/dash-trips-summary.html', context)



@login_required
def trips_dashboard_ratings_view(request):

    if request.user.profile.user_type == "passenger":
        user_profile=request.user.profile.passenger_profile
    elif request.user.profile.user_type == "driver":
        user_profile=request.user.profile.driver_profile

    trips = user_profile.trips_passenger.filter(status='completed')
    user_profile.update_rating(trips)

    print("user_profile")
    print(request.user.profile.passenger_profile.count_rating)

    context = {
        'user_profile': user_profile,
        'rating_levels': user_profile.get_rating_levels(trips)
    }

    print("Conteeeeeeeeeeeeeeeeeeeeeeetx below")
    print(context['rating_levels'])
    return render(request, 'trips/partials/dash-ratings.html',context)



@login_required
def trips_list_view(request, filter_trips='all'):

    if filter_trips == "recent":
        if request.user.profile.user_type == "passenger":
            trips = Trip.objects.filter(
                    passenger=request.user.profile.passenger_profile,
                ).order_by('-updated_on')[:4]
        elif request.user.profile.user_type == "driver":
            trips = Trip.objects.filter(
                    driver=request.user.profile.driver_profile,
                ).order_by('-updated_on')[:4]

        context = {
            'trips': trips,
            'user': request.user,
        }

        return render(request, 'trips/partials/dash-table.html', context)

    else:

        if request.user.profile.user_type == "passenger":
            trips = Trip.objects.filter(
                    passenger=request.user.profile.passenger_profile,
                ).order_by('travel_datetime')
        elif request.user.profile.user_type == "driver":
            trips = Trip.objects.filter(
                    driver=request.user.profile.driver_profile,
                ).order_by('travel_datetime')

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

    if request.user.profile.user_type == "passenger":
        user_trip_rating = trip.passenger_rating
    elif request.user.profile.user_type == "driver":
        user_trip_rating = trip.driver_rating

    context = {
        'trip': trip,
        'user': request.user,
        'is_modal': is_modal,
        'user_trip_rating': user_trip_rating,
        'ratings_num': range(1, 6),
    }
    return render(request, 'trips/partials/trip-detail.html', context)


@login_required
def trip_request_view(request):

    if request.method == "POST":
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

    trip = get_object_or_404(Trip, trip_name=trip_name)
    # chek if trip allows edits
    check_action_allowed(trip)

    if request.method == "POST":
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

    if request.method == "POST":
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

# DriverRatingForm PassengerRatingForm


@login_required
def rate_trip_view(request, trip_name):

    trip = get_object_or_404(Trip, trip_name=trip_name)

    # Handle form submission
    if request.method == "POST":
        if request.user.profile.user_type == "passenger":
            form = PassengerRatingForm(request.POST, instance=trip)
        elif request.user.profile.user_type == "driver":
            form = DriverRatingForm(request.POST, instance=trip)
        else:
            print("Error - page not found")  # change to 404 error page

        if form.is_valid():
            # mioght revise if any fields is missing
            form.save()

            # trigger new event - ratingsUpdated
            return HttpResponse(status=204)

    if request.user.profile.user_type == "passenger":
        form = PassengerRatingForm(instance=trip)
        rating_user = trip.passenger.profile.user
        rated_user = trip.driver.profile.user
    elif request.user.profile.user_type == "driver":
        form = DriverRatingForm(instance=trip)
        rating_user = trip.driver.profile.user
        rated_user = trip.passenger.profile.user
    else:
        print("Error - page not found")  # change to 404 error page

    context = {
        'form': form,
        'trip': trip,
        'user': request.user,
        'rating_user': rating_user,
        'rated_user': rated_user,
    }

    return render(request, 'trips/trip-ratings.html', context)

# Drriver availability wrt trips:


@login_required
def driver_availability_view(request):

    if request.user.profile.user_type == "driver":
        trips = Trip.objects.filter(
                driver=request.user.profile.driver_profile,
            )
    else:
        print("Error: You are not a driver! Dont try trick us!!")

    context = {
        'events': trips,
    }

    return render(request, 'users/driver-availability.html', context)


@login_required
def allocated_trips(request):
    if request.user.profile.user_type == "driver":
        trips = Trip.objects.filter(
                driver=request.user.profile.driver_profile,
            )
    else:
        print("Error: You are not a driver! Dont try trick us!!")

    trips_list = []

    for trip in trips:

        trips_list.append({
            'id': trip.id,
            'start': trip.travel_datetime.isoformat(),
            # 'location_end': trip.location_end,
            # 'title': trip.trip_type,
            'title': ''.join([word[0] for word in trip.trip_type.split()]),
            # 'type': trip.trip_type,
            # 'status': trip.status,
            'className': f'status-{trip.status_class}',

        })

    return JsonResponse(trips_list, safe=False)


@login_required
def driver_action_view(request, trip_name):

    trip = get_object_or_404(Trip, trip_name=trip_name)

    # ensure user driver on this trip:
    if request.user.profile.user_type == "driver" and trip.driver.profile.user == request.user:
        if request.method == "POST":
            if trip.status == 'confirmed':
                trip.start_trip()
            elif trip.status == 'in_progress':
                trip.end_trip()
            else:
                return HttpResponseForbidden("Action not authorized for this trip.")

            return HttpResponse(status=204, headers={'HX-trigger': 'tripListChanged'})

        context = {
        'trip': trip,
        'user': request.user
        }

        if trip.status == 'confirmed':
            return render(request, 'trips/trip-start.html', context)
        elif trip.status == 'in_progress':
            return render(request, 'trips/trip-end.html', context)
        else:
            return HttpResponseForbidden("Action not authorized for this trip.")

    else:
        return HttpResponseForbidden("Action not authorized for this trip.")


@login_required
def admin_all_view(request):
    return render(request, 'trips/admin-all.html')


@login_required
def admin_trips_view(request):
    trips =Trip.objects.all()
    context = {
        'trips': trips,
    }
    return render(request, 'trips/partials/admin-trips.html',context)


@login_required
def admin_passengers_view(request):
    passengers =PassengerProfile.objects.all()

    for passenger in passengers:
        passenger.update_rating(passenger.trips_passenger.filter(status='completed'))

    context = {
        'passengers': passengers,
    }
    return render(request, 'trips/partials/admin-passengers.html',context)


@login_required
def admin_drivers_view(request):
    drivers =DriverProfile.objects.all()
    context = {
        'drivers': drivers,
    }
    return render(request, 'trips/partials/admin-drivers.html',context)