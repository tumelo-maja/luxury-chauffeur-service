from django.urls import path
from .views import *

urlpatterns = [
    path('', trips_page_view, name="trips"),
    path('trips-list/<filter_trips>/', trips_list_view, name="trips-list"),
    path('details/<partial>', dash_details_view, name="dash-details"),
    path('edit/<trip_name>/', trip_edit_view, name="trip-edit"),
    path('delete/<trip_name>/', trip_delete_view, name="trip-delete"),
    path('request/', trip_request_view, name="trip-request"),
    path('trip/<trip_name>', trip_detail_view, name="trip-detail"),
    path('feedback/<trip_name>', rate_trip_view, name="trip-feedback"),
    path('driver/<trip_name>/', driver_action_view, name="trip-action"),
    path('calendar/', trips_calendar_view, name='trips-calendar'),
    path('calendar/subsets/', trips_calendar_subsets_view, name='trips-calendar-subsets'),
    path('manager/', manager_overview_view, name='manager-overview'),
    path('manager/<tab_name>/', manager_tabs_view, name='manager-tabs'),
    path('review/<trip_name>/', trip_review_view, name="trip-review"),
]
