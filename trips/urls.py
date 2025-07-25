from django.urls import path
from .views import *

urlpatterns = [
    path('', trip_view, name="trips"),
    path('trips-list/<filter_trips>/', trips_list_view, name="trips-list"),
    path('dashboard/', trips_dashboard_view, name="trips-dashboard"),
    path('dashboard/details/<partial>', dash_details_view, name="dash-details"),
    path('dashboard/stats/', trips_dashboard_stats_view, name="trips-dashboard-stats"),
    path('dashboard/ratings/', trips_dashboard_ratings_view, name="trips-ratings"),
    path('edit/<trip_name>/', trip_edit_view, name="trip-edit"),
    path('delete/<trip_name>/', trip_delete_view, name="trip-delete"),
    path('request/', trip_request_view, name="trip-request"),
    path('trip/<trip_name>', trip_detail_view, name="trip-detail"),
    path('feedback/<trip_name>', rate_trip_view, name="trip-feedback"),
    path('driver/<trip_name>/', driver_action_view, name="trip-action"),
    path('availability/', driver_availability_view, name='driver-availability'),
    path('admin/', admin_all_view, name='admin-all'),
    path('admin/trips/', admin_trips_view, name='admin-trips'),
    path('admin/passengers/', admin_passengers_view, name='admin-passengers'),
    path('admin/drivers/', admin_drivers_view, name='admin-drivers'),
]
