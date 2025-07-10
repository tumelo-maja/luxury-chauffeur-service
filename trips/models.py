from django.db import models
import shortuuid
from users.models import DriverProfile, PassengerProfile

# Create your models here.

# CONSTANTS
VEHICLE_CHOICES = [
    ("Rolls Royce Phantom", "Rolls Royce Phantom"),
    ("Range Rover Vogue", "Range Rover Vogue"),
    ("Mercedes Benz V-Class", "Mercedes Benz V-Class"),
    ("Premium Limousine", "Premium Limousine"),
    ("Classic Vintage Cars", "Classic Vintage Cars"),
]

TRIP_TYPES = [
        ("Airport Transfers", "Airport Transfers"),
        ("Special Events", "Special Events"),
        ("Corporate Chauffeur", "Corporate Chauffeur"),
        ("Private & VIP Chauffeur", "Private & VIP Chauffeur"),
    ]

STATUS_OPTIONS = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("in_progress", "In progress"),
        ("cancelled", "Cancelled"),
        ("modified", "Modified"),
        ("completed", "Completed"),
    ]


class Trip(models.Model):
    trip_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    passenger = models.ForeignKey(PassengerProfile, on_delete=models.CASCADE, related_name='trips_passenger')
    location_start = models.CharField(max_length=200)
    location_end = models.CharField(max_length=200)
    travel_datetime = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    trip_type = models.CharField(max_length=50, choices=TRIP_TYPES)
    comments = models.TextField(blank=True, null=True)
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='trips_driver')

    status = models.CharField(max_length=50, choices=STATUS_OPTIONS, default="pending")

    vehicle = models.CharField(max_length=100, choices=VEHICLE_CHOICES)

    class Meta:
        ordering = ["-travel_datetime"]

    def __str__(self):
        return f"Trip {self.id} for {self.passenger} - {self.location_end} ({self.travel_datetime})"
    
    @property
    def status_class(self):
        return self.status.replace('_', '-').lower()

    @property
    def status_str(self):
        return self.status.replace('_', ' ').capitalize()    
