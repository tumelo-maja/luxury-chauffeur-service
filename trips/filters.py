import django_filters
from .models import Trip, STATUS_OPTIONS

class TripFilter(django_filters.FilterSet):

    status_type = django_filters.ChoiceFilter(
        choices=STATUS_OPTIONS,
        field_name = 'status',
        lookup_expr = 'iexact',
        empty_label="All")

    class Meta:
        model = Trip
        fields = ('status_type',)
