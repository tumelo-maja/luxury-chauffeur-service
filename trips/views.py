from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Trip
from users.models import PassengerProfile, DriverProfile
from .forms import *


@login_required
def trips_dashboard_view(request):
    """
    Display the main dashboard page.

    Returns
    -------
    Rendered dashboard page (default - home display).
    """
    return render(request, 'trips/trips-dashboard.html')


@login_required
def dash_details_view(request, partial):
    """
    Switches dashboard view using partials for a given section.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.
    partial : str
        The dashboard section to render; passed as query parameter in the template

    Returns
    -------
    Rendered dashboard partial template.
    For the 'home' partial, context is rendered for the summary display
    """
    context={}

    if partial == 'home':
        status_completed='completed'
        user_status = request.user.profile.status

        if request.user.profile.user_type == "passenger":
            user_profile = request.user.profile.passenger_profile
            trips = Trip.objects.filter(passenger=request.user.profile.passenger_profile)
            trips_completed = trips.filter(status=status_completed)
            
        elif request.user.profile.user_type == "driver":
            user_profile = request.user.profile.driver_profile
            trips = Trip.objects.filter(driver=request.user.profile.driver_profile)
            trips_completed = trips.filter(status=status_completed)

        elif request.user.profile.user_type == "manager":
            user_profile = request.user.profile.manager_profile
            trips = Trip.objects.all()
            trips_completed = trips.filter(status=status_completed)

        user_profile.update_rating(trips_completed)

        context = {
            'user_profile': user_profile,
            'rating_levels': user_profile.get_rating_levels(trips_completed),
            'user_status': user_status,
            'stats': {
                'cancelled': trips.filter(status='cancelled').count(),
                'completed': trips_completed.count(),
                'pending': trips.filter(status='pending').count(),
                'modified': trips.filter(status='modified').count(),
            },            
        }
        
    return render(request, f'trips/partials/dash-{partial}.html',context)


@login_required
def trips_list_view(request, filter_trips='all'):
    """
    Display a list of role-specific trips for the current user.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.
    filter_trips : str
        Filter option ('recent' or 'all'), by default 'all'.

    Returns
    -------
    Rendered trips list template.
    """
    if filter_trips == "recent":
        if request.user.profile.user_type == "passenger":
            trips = Trip.objects.filter(
                passenger=request.user.profile.passenger_profile,
            ).order_by('-updated_on')[:4]
        elif request.user.profile.user_type == "driver":
            trips = Trip.objects.filter(
                driver=request.user.profile.driver_profile,
            ).order_by('-updated_on')[:4]
        elif request.user.profile.user_type == "manager":
            trips = Trip.objects.all().order_by('-updated_on')[:4]

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
        elif request.user.profile.user_type == "manager":
            trips = Trip.objects.all().order_by('travel_datetime')

        context = {
            'trips': trips,
            'user': request.user
        }

        return render(request, 'trips/trips-list.html', context)


@login_required
def trip_detail_view(request, trip_name):
    """
    Displays a modal containing detailed information for a specific trip.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.
    trip_name : str
        Unique identifier of the trip.

    Returns
    -------
    Rendered trip details modal.
    """
    queryset = Trip.objects.filter(trip_name=trip_name)
    trip = get_object_or_404(queryset)

    is_modal = request.GET.get('modal', 'true') == 'true'

    if request.user.profile.user_type == "passenger":
        user_trip_rating = trip.passenger_rating
    elif request.user.profile.user_type == "driver":
        user_trip_rating = trip.driver_rating
    elif request.user.profile.user_type == "manager":
        user_trip_rating = None

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
    """
    Displays a modal containing a trip request view. 
    Handles trip creating trip requests

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.

    Returns
    -------
    Rendered trip request form in a modal or 204 response if successfully submitted.
    """
    if request.method == "POST":
        form = TripRequestForm(request.POST)
        form = check_trip_overlap(request.user.profile.passenger_profile, form)

        if form.is_valid():

            trip = form.save(commit=False)
            trip.passenger = request.user.profile.passenger_profile
            trip.save()

            return HttpResponse(status=204, headers={'HX-trigger': 'tripListChanged'})

        else:
            context = {
                'form': form,
            }
            return render(request, 'trips/trip-request.html', context)            

    else:
        form = TripRequestForm()


        driver_id = request.GET.get('driver')
        if driver_id:
            form.fields['driver'].initial = driver_id

        trip_type = request.GET.get('trip-type')
        if trip_type:
            form.fields['trip_type'].initial = trip_type

        vehicle = request.GET.get('vehicle')
        if vehicle:
            form.fields['vehicle'].initial = vehicle
        
        trip_datetime = request.GET.get('datetime')
        if trip_datetime:
            form.fields['travel_datetime'].initial = datetime.strptime(trip_datetime, '%Y-%m-%dT%H:%M')


    min_valid_time = datetime.now() + timedelta(hours=1)
    min_valid_time_str = min_valid_time.strftime('%Y-%m-%dT%H:%M')

    context = {
        'form': form,
        'min_valid_time_str': min_valid_time_str,
    }
    return render(request, 'trips/trip-request.html', context)

def check_trip_overlap(passenger, form):
    """
    Validate the passenger has another trip scheduled within one hour of the current request.
    1-hour window is defined locally, a window is created -1hr and +1hr of `travel_datetime`

    Parameters
    ----------
    passenger : int or UUID
        The primary key (ID) of the passenger making the trip request.
    form : TripRequestForm
        The submitted form instance containing the `travel_datetime` field.

    Returns
    -------
    forms
        The same form instance, with an error added to `travel_datetime` if a conflicting trip exists.
    """  
    raw_datetime = form.data.get("travel_datetime")
    travel_datetime = timezone.make_aware(parse_datetime(raw_datetime))

    timedelta_window = timedelta(minutes=60)
    window_start = travel_datetime - timedelta_window
    window_end = travel_datetime + timedelta_window

    trips_in_window = Trip.objects.filter(passenger_id= passenger,travel_datetime__range=(window_start, window_end)).exists()

    if trips_in_window:
        form.add_error("travel_datetime","You already have another trip scheduled within 1 hour of this time.")

    return form   

@login_required
def trip_edit_view(request, trip_name):
    """
    Displays a modal containing a trip edit view. 
    Handles trip editing trip existing requests

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.
    trip_name : str
        Unique identifier of the trip to be modified.

    Returns
    -------
    Rendered pre-filled trip edit form in a modal or 204 response if successfully submitted.
    """
    trip = get_object_or_404(Trip, trip_name=trip_name)

    if request.method == "POST":
        form = TripRequestForm(request.POST, instance=trip)
        if form.is_valid():

            trip = form.save(commit=False)
            trip.status = "modified"
            trip.passenger = request.user.profile.passenger_profile
            trip.save()

            messages.success(request, "Changes saved successfully.")

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
    """
    Displays a confirmation modal for canceling an existing trip. 
    Handles trip editing trip existing requests

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object.
    trip_name : str
        Unique identifier of the trip to be cancelled.

    Returns
    -------
    Rendered trip cancel confirmation form in a modal or 204 response if successfully submitted.
    """
    trip = get_object_or_404(Trip, trip_name=trip_name)

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


@login_required
def trip_review_view(request, trip_name):

    trip = get_object_or_404(Trip, trip_name=trip_name)

    if request.method == "POST":
        form = TripRequestForm(instance=trip)
        request_outcome = request.POST.get('request_outcome')
        trip = form.save(commit=False)

        if request_outcome == 'reject':
            trip.status = "rejected"
        elif request_outcome == 'approve':
            trip.status = "confirmed"

        trip.save()

        return HttpResponse(status=204, headers={'HX-trigger': 'tripStatusChanged'})

    else:
        form = TripRequestForm(instance=trip)

    # only driver fieldcan be changed
    for field_name, field in form.fields.items():
        if field_name != 'driver':
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
            field.required = False

    # check indicators to display
    travel_datetime = trip.travel_datetime
    check_window_hrs = 6
    start_time = travel_datetime - timedelta(hours=check_window_hrs)
    end_time = travel_datetime + timedelta(hours=check_window_hrs)

    driver_window_trips = Trip.objects.filter(
        driver=trip.driver,
        travel_datetime__gte=start_time,
        travel_datetime__lt=end_time
    ).exclude(trip_name=trip.trip_name)

    passenger_window_trips = Trip.objects.filter(
        passenger=trip.passenger,
        travel_datetime__gte=start_time,
        travel_datetime__lt=end_time
    ).exclude(trip_name=trip.trip_name)

    # warning texts list
    warning_texts = []
    if driver_window_trips.count():
        warning_texts.append(
            f"The driver has {driver_window_trips.count()} other trips within {check_window_hrs} hours of this time:")

    if passenger_window_trips.count():
        warning_texts.append(
            f"The passenger has {passenger_window_trips.count()} other trip(s) within {check_window_hrs} hours of this time:")

    context = {
        'trip': trip,
        'form': form,
        'user': request.user,
        'warning_texts': warning_texts,
        'driver_window_trips': driver_window_trips,
        'passenger_window_trips': passenger_window_trips,
    }

    return render(request, 'trips/trip-review.html', context)


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
def trips_calendar_view(request):
    return render(request, 'trips/partials/dash-calendar.html')


@login_required
def trips_calendar_subsets_view(request):

    # get today date
    today = datetime.today()

    current_year = today.year
    current_month = today.month

    year = int(request.GET.get('year', current_year))
    month = int(request.GET.get('month', current_month))

    start_datetime = timezone.make_aware(datetime(year, month, 1, 0, 0, 0))
    if month == 12:
        end_datetime = timezone.make_aware(datetime(year + 1, 1, 1, 0, 0, 0))
    else:
        end_datetime = timezone.make_aware(
            datetime(year, month + 1, 1, 0, 0, 0))

    trips = Trip.objects.filter(
        travel_datetime__gte=start_datetime,
        travel_datetime__lt=end_datetime
    )

    monthly_trips = [{'travel_datetime': trip.travel_datetime.date().isoformat(),
                      'travel_date': trip.travel_datetime.strftime("%d/%m/%Y"), }
                     for trip in trips]

    return JsonResponse({'trips': monthly_trips})


@login_required
def allocated_trips(request):

    trips_list = []
    if request.user.profile.user_type == "driver":
        trips = Trip.objects.filter(
            driver=request.user.profile.driver_profile,
        )

        for trip in trips:

            trip_type = ''.join([word[0] for word in trip.trip_type.split()])
            trip_time = trip.travel_datetime.strftime("%H:%M")

            trips_list.append({
                'id': trip.trip_name,
                'start': trip.travel_datetime.isoformat(),
                'title': f'<span class="time">{trip_time}</span><span class="title">{trip_type}</span>',
                'className': f'status-{trip.status_class} clickable',

            })

        return JsonResponse(trips_list, safe=False)

    elif request.user.profile.user_type == "manager":
        trips = Trip.objects.all()

        daily_trips_count = {}
        for trip in trips:
            date = trip.travel_datetime.date()
            status = trip.status

            # intialise date key if it doesnt exit yet
            if date not in daily_trips_count:
                daily_trips_count[date] = 0
            daily_trips_count[date] += 1

        for date, trip_counts in daily_trips_count.items():
            trips_list.append({
                'start': date.isoformat(),
                'title': f"{trip_counts} x {'trip' if trip_counts == 1 else 'trips'}",
                'className': f"{status} clickable",
            })

        return JsonResponse(trips_list, safe=False)

    else:
        print("Error: You are not a driver! nor a Manager! Dont try trick us!!")
        return JsonResponse(trips_list, safe=False)


@login_required
def driver_action_view(request, trip_name):

    trip = get_object_or_404(Trip, trip_name=trip_name)

    # ensure user driver on this trip:
    if request.user.profile.user_type == "driver" and trip.driver.profile.user == request.user:
        if request.method == "POST":
            if trip.status == 'confirmed':
                trip.start_trip()
                request.user.profile.update_status('engaged')
            elif trip.status == 'in_progress':
                trip.end_trip()
                request.user.profile.update_status('available')
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
def manager_all_view(request):
    return render(request, 'trips/manager-all.html')


@login_required
def manager_tabs_view(request, tab_name):

    if tab_name == "trips":
        trips = Trip.objects.all()
        context = {
            'trips': trips,
        }
        return render(request, 'trips/partials/manager-trips.html', context)

    elif tab_name == "passengers":
        passengers = PassengerProfile.objects.all()

        for passenger in passengers:
            passenger.update_rating(
                passenger.trips_passenger.filter(status='completed'))

        context = {
            'passengers': passengers,
        }
        return render(request, 'trips/partials/manager-passengers.html', context)

    elif tab_name == "drivers":
        drivers = DriverProfile.objects.all()
        context = {
            'drivers': drivers,
        }
        return render(request, 'trips/partials/manager-drivers.html', context)
