from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from users.models import Profile, DriverProfile, PassengerProfile, ManagerProfile
from ..models import Trip


class TripsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # password for all
        cls.users_password = "TheUltimateTester2025"
        # create passenger
        cls.user_passenger = User.objects.create_user(
            username="passenger1", password=cls.users_password, email="passenger1@luxtest.com",)
        cls.profile_passenger = PassengerProfile.objects.create(
            profile=Profile.objects.get(user=cls.user_passenger))
        cls.profile_passenger.profile.user_type = "passenger"

        # create driver
        cls.user_driver = User.objects.create_user(
            username="driver1", password=cls.users_password, email="driver1@luxtest.com",)
        cls.profile_driver = DriverProfile.objects.create(
            profile=Profile.objects.get(user=cls.user_driver))
        cls.profile_driver.profile.user_type = "driver"

        # create manager
        cls.user_manager = User.objects.create_user(
            username="manager1", password=cls.users_password, email="manager1@luxtest.com",)
        cls.profile_manager = ManagerProfile.objects.create(
            profile=Profile.objects.get(user=cls.user_manager))
        cls.profile_manager.profile.user_type = "manager"

        # trips urls
        cls.trip_request_url = reverse("trip-request")

        # choice variables
        cls.vehicle_choices = ["Rolls Royce Phantom", "Range Rover Vogue",
                               "Mercedes Benz V-Class", "Premium Limousine", "Classic Vintage Cars",]
        cls.trip_types = ["Airport Transfers", "Special Events",
                          "Corporate Chauffeur", "Private & VIP Chauffeur",]

    def login_user(self, user_type):
        self.client.login(
            username=f"{user_type}1",
            password=self.users_password)

    def test_passenger_can_create_a_trip(self):
        self.login_user('passenger')

        self.assertFalse(Trip.objects.filter(passenger=self.profile_passenger).exists())  # no trips

        # create trip
        self.trip = Trip.objects.create(
            passenger=self.profile_passenger,
            driver=self.profile_driver,
            location_start="Heathrow Airport",
            location_end="Lux Hotel",
            travel_datetime=parse_datetime("2025-09-21T15:30:00Z"),
            trip_type="Airport Transfers",
            vehicle="Range Rover Vogue",
        )

        self.assertTrue(Trip.objects.filter(passenger=self.profile_passenger).exists())  # 1 trip

