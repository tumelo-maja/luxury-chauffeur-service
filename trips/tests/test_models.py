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
    
    def create_test_trip(self):
        self.login_user('passenger')

        self.trip = Trip.objects.create(
            passenger=self.profile_passenger,
            driver=self.profile_driver,
            location_start="Heathrow Airport",
            location_end="Lux Hotel",
            travel_datetime=parse_datetime("2025-09-21T15:30:00Z"),
            trip_type="Airport Transfers",
            vehicle="Range Rover Vogue",
        )        

    def create_test_trip_for_driver(self):
        self.create_test_trip()
        self.client.logout()
        self.login_user('driver')

    def test_passenger_can_create_a_trip(self):
        self.login_user('passenger')

        self.assertFalse(Trip.objects.filter(passenger=self.profile_passenger).exists())  # no trips

        # create trip
        Trip.objects.create(
            passenger=self.profile_passenger,
            driver=self.profile_driver,
            location_start="Heathrow Airport",
            location_end="Lux Hotel",
            travel_datetime=parse_datetime("2025-09-21T15:30:00Z"),
            trip_type="Airport Transfers",
            vehicle="Range Rover Vogue",
        )

        self.assertTrue(Trip.objects.filter(passenger=self.profile_passenger).exists())  # 1 trip

    def test_newly_created_trip_has_status_of_pending(self):
        #New trips should have a default status of 'pending'
        self.login_user('passenger')
        self.create_test_trip()

        self.assertEqual(self.trip.status,'pending')

    def test_status_class_property_replaces_underscore_with_dashes(self):
        # status_class replaces underscores with dashes
        self.create_test_trip()

        self.trip.status = "in_progress"
        self.assertEqual(self.trip.status_class, "in-progress")

    def test_status_str_property_replaces_underscore_with_spaces(self):
        # status_class replaces underscores with spaces and capitalizes
        self.create_test_trip()

        self.trip.status = "in_progress"
        self.assertEqual(self.trip.status_str, "In progress")

    def test_driver_is_assigned_to_a_trip_on_trip_creation(self):
        self.assertFalse(Trip.objects.filter(driver=self.profile_driver).exists())  # no trips
        self.create_test_trip()
        self.client.logout()

        self.login_user('driver')
        self.assertTrue(Trip.objects.filter(driver=self.profile_driver).exists())  # 1 trip

    def test_start_trip_method_changes_trip_status_to_in_progress(self):
        self.create_test_trip_for_driver()
        self.assertEqual(self.trip.status,'pending')

        self.trip.start_trip()
        self.assertEqual(self.trip.status,'in_progress')

    def test_start_trip_method_changes_passenger_and_driver_status_to_engaged(self):
        self.create_test_trip_for_driver()
        self.assertEqual(self.trip.driver.profile.status,'available')
        self.assertEqual(self.trip.passenger.profile.status,'available')

        self.trip.start_trip()
        self.assertEqual(self.trip.driver.profile.status,'engaged')
        self.assertEqual(self.trip.passenger.profile.status,'engaged')

    def test_end_trip_method_changes_trip_status_to_completed(self):
        self.create_test_trip_for_driver()

        self.trip.start_trip()
        self.assertEqual(self.trip.status,'in_progress')

        self.trip.end_trip()
        self.assertEqual(self.trip.status,'completed')

    def test_end_trip_method_changes_passenger_and_driver_status_to_available(self):
        self.create_test_trip_for_driver()

        self.trip.start_trip()
        self.assertEqual(self.trip.driver.profile.status,'engaged')
        self.assertEqual(self.trip.passenger.profile.status,'engaged')

        self.trip.end_trip()
        self.assertEqual(self.trip.driver.profile.status,'available')
        self.assertEqual(self.trip.passenger.profile.status,'available')