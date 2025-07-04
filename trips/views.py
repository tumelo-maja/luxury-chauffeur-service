from django.shortcuts import render, get_object_or_404
from .models import Trip

# Create your views here.


def trip_view(request):
    # get all trips and filter for logged in user
    trips = Trip.objects.filter(passenger=request.user)

    context = {
        'trips': trips,
        'user': request.user
    }

    return render(request, 'trips/trip.html', context)


def trip_detail_view(request, trip_name):

    queryset = Trip.objects.filter(trip_name=trip_name)
    trip = get_object_or_404(queryset)

    context = {
        'trip': trip,
        'user': request.user,
        }
    return render(request, 'trips/partials/trip-detail.html', context)
