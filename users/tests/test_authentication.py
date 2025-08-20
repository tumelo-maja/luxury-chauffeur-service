from django.test import TestCase
from django.urls import reverse
import os
from django.contrib.auth.models import User

class TestUsersAuthentication(TestCase):
    def setUp(self):
        self.signup_type_url = reverse("signup_type")
        self.signup_driver_url = reverse("user_signup", query={'role':'driver',})
        self.signup_passenger_url = reverse("user_signup", query={'role':'passenger',})

        self.login_url = reverse("account_login")
        self.logout_url = reverse("account_logout")

        self.signup_passenger_valid_data= {
            "username": "passenger1",
            "first_name": "Passenger1",
            "last_name": "Tester",
            "email": "passenger1@luxtest.com",
            "password1": "TheUltimateTester2025",
            "password2": "TheUltimateTester2025",
            "role": "passenger",
        }

    def test_passenger_signup_valid_data(self):
        #test signup for passenger 
        response = self.client.post(reverse("user_signup", query={'role':'passenger',}), self.signup_passenger_valid_data, follow=True)

        self.assertTrue(User.objects.filter(username="passenger1").exists()) # is user saved?
        self.assertRedirects(response, reverse("account-success")) # redirected to success page?
        self.assertContains(response, "Please check your inbox to activate your account.", status_code=200) # status=200? text content

