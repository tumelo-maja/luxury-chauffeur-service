from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from users.models import Profile, DriverProfile, PassengerProfile

class UsersProfileModelTests(TestCase):

    def setUp(self):
        self.signup_passenger_valid_data= {
            "username": "passenger1",
            "first_name": "Passenger1",
            "last_name": "Tester",
            "email": "passenger1@luxtest.com",
            "password1": "TheUltimateTester2025",
            "password2": "TheUltimateTester2025",
            "role": "passenger",
        } 

        # define urls as properties/attr
        signup_passenger_url = reverse("user_signup", query={'role':'passenger',})
        self.login_url = reverse("account_login")
        self.profile_edit_url =reverse("profile-edit")
             
        self.client.post(signup_passenger_url, self.signup_passenger_valid_data)
        self.client.login(
            username=self.signup_passenger_valid_data['username'], 
            password=self.signup_passenger_valid_data['password1'])
        
        self.user = User.objects.get(username=self.signup_passenger_valid_data['username'])
        self.profile = Profile.objects.get(user=self.user)

    def test_name_property_returns_username_if_no_displayname(self):
        self.profile.displayname = ""
        self.assertEqual(self.profile.name, "passenger1")
        
    def test_name_property_returns_displayname_if_set(self):
        self.profile.displayname = "Nick Name"
        self.assertEqual(self.profile.name, "Nick Name")

    def test_update_status_method_changes_the_status_attribute(self):
        self.assertEqual(self.profile.status, "available")
        self.profile.update_status("engaged")
        self.assertEqual(self.profile.status, "engaged")


    
