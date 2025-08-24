from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import timedelta, datetime
from django.http import Http404
from users.models import Profile, DriverProfile, PassengerProfile, ManagerProfile
from ..models import Trip
from ..forms import *


class TripsFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # password for all
        cls.users_password = "TheUltimateTester2025"
        # create passenger
        cls.user_passenger = User.objects.create_user(
            username="passenger1", password=cls.users_password, email="passenger1@luxtest.com",)
        pass_profile = Profile.objects.get(user=cls.user_passenger)
        pass_profile.user_type = "passenger"
        pass_profile.save()
        cls.profile_passenger = PassengerProfile.objects.create(
            profile=pass_profile)
        cls.profile_passenger.profile.user_type = "passenger"

        # create driver
        cls.user_driver = User.objects.create_user(
            username="driver1", password=cls.users_password, email="driver1@luxtest.com",)
        drive_profile = Profile.objects.get(user=cls.user_driver)
        drive_profile.user_type = "driver"        
        drive_profile.save()
        cls.profile_driver = DriverProfile.objects.create(
            profile=drive_profile)
        cls.profile_driver.profile.user_type = "driver"

        # create manager
        cls.user_manager = User.objects.create_user(
            username="manager1", password=cls.users_password, email="manager1@luxtest.com",)
        man_profile = Profile.objects.get(user=cls.user_manager)
        man_profile.user_type = "manager"        
        man_profile.save()
        cls.profile_manager = ManagerProfile.objects.create(
            profile=man_profile)
        cls.profile_manager.profile.user_type = "manager"

        # url paths
        cls.trips_url = reverse("trips")
        cls.trip_request_url = reverse("trip-request")
        cls.login_url = reverse("account_login")
        cls.login_url = reverse("account_login")
        cls.dash_details_url ='dash-details'
        cls.trip_detail_url = "trip-detail"
        cls.trip_edit_url = "trip-edit"
        cls.trip_cancel_url = "trip-cancel"
        cls.trip_feedback_url = "trip-feedback"
        cls.trip_action_url = "trip-action"
        cls.trip_review_url = "trip-review"
        cls.trip_manager_overview_url = reverse("manager-overview")

        # choice variables
        cls.vehicle_choices = ["Rolls Royce Phantom", "Range Rover Vogue",
                               "Mercedes Benz V-Class", "Premium Limousine", "Classic Vintage Cars",]
        cls.trip_types = ["Airport Transfers", "Special Events",
                          "Corporate Chauffeur", "Private & VIP Chauffeur",]
        
        cls.form_data = {
                    "location_start": "Lux Hotel",
                    "location_end": "Lux International Airport",
                    "travel_datetime": datetime.now()+ timedelta(days=1, hours=2),
                    "driver": cls.profile_driver.id,
                    "vehicle": cls.vehicle_choices[2],
                    "trip_type": cls.trip_types[1],
                }


    def login_user(self, user_type):
        self.client.login(
            username=f"{user_type}1",
            password=self.users_password)
        self.user = User.objects.get(username=f"{user_type}1")
    
    def test_passenger_can_submit_a_valid_trip_request(self):
        
        self.login_user('passenger')

        response = self.client.post(self.trip_request_url, self.form_data)
        self.assertTrue(Trip.objects.filter(passenger=self.profile_passenger).exists())
        self.assertEqual(response.status_code, 204)






    


