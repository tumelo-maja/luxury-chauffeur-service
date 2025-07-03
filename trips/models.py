from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Trip(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    location_start = models.CharField(max_length=200)
    location_end = models.CharField(max_length=200)
    travel_date = models.DateField()
    travel_time = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    TRIP_TYPES = [
        ("Airport Transfers", "Airport Transfers"),
        ("Special Events", "Special Events"),
        ("Corporate Chauffeur", "Corporate Chauffeur"),
        ("Private & VIP Chauffeur", "Private & VIP Chauffeur"),
    ]
    trip_type = models.CharField(max_length=50, choices=TRIP_TYPES)
    comments = models.TextField(blank=True, null=True)

    INTERIM_DRIVERS = [
        ("John Doe", "John Doe"),
        ("Jane Smith", "Jane Smith"),
        ("Michael Johnson", "Michael Johnson"),
        ("Emily Davis", "Emily Davis"),
        ("Chris Brown", "Chris Brown"),
    ]

    driver = models.CharField(max_length=50, choices=INTERIM_DRIVERS)

    STATUS_OPTIONS = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("in_progress", "In Progress"),
        ("cancelled", "Cancelled"),
        ("modified", "Modified"),
        ("completed", "Completed"),
    ]
    status = models.CharField(
        max_length=50, choices=STATUS_OPTIONS, default="pending")

    class Meta:
        ordering = ["-travel_date"]

    def __str__(self):
        return f"Trip {self.id} for {self.passenger} - {self.location_end} ({self.travel_date} {self.travel_time})"
