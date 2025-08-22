from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from users.models import Profile, DriverProfile, PassengerProfile, ManagerProfile
from ..models import Trip


class TripsViewTest(TestCase):

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

        # url paths
        cls.trips_url = reverse("trips")
        cls.trip_request_url = reverse("trip-request")
        cls.login_url = reverse("account_login")
        cls.dash_details_url ='dash-details'

        # choice variables
        cls.vehicle_choices = ["Rolls Royce Phantom", "Range Rover Vogue",
                               "Mercedes Benz V-Class", "Premium Limousine", "Classic Vintage Cars",]
        cls.trip_types = ["Airport Transfers", "Special Events",
                          "Corporate Chauffeur", "Private & VIP Chauffeur",]

    def login_user(self, user_type):
        self.client.login(
            username=f"{user_type}1",
            password=self.users_password)
    
    def test_unauthenticated_users_are_redirected_to_login_when_accessing_trips_page(self):
        response = self.client.get(self.trips_url)
        self.assertRedirects(response, expected_url=f"{self.login_url}?next={self.trips_url}")

    def test_authenticated_users_can_access_trips_page(self):
        self.login_user('passenger')
        response = self.client.get(self.trips_url)
        self.assertContains(response, "Manage your trips with ease.", status_code=200) 

    def test_trips_page_uses_correct_template(self):
        #test template rendered
        self.login_user('passenger')
        response = self.client.get(self.trips_url)
        self.assertTemplateUsed(response, "trips/trips.html")

    def test_correct_headings_are_rendered_in_trips_summary_view(self):
        #test template rendered
        self.login_user('passenger')
        response = self.client.get(reverse(self.dash_details_url,args=['home']))
        self.assertContains(response, "Trips Summary") 
        self.assertContains(response, "Ratings") 
        self.assertContains(response, "Recent Activities") 

    def test_trips_list_view_rendered_correctly(self):
        #test template rendered
        self.login_user('passenger')
        response = self.client.get(reverse(self.dash_details_url,args=['list-view']))
        self.assertContains(response, "My trips") 

    def test_trips_calendar_view_rendered_correctly(self):
        #test template rendered
        self.login_user('passenger')
        response = self.client.get(reverse(self.dash_details_url,args=['calendar-view']))
        self.assertContains(response, "userCalendar") 
        self.assertContains(response, "Wed")         