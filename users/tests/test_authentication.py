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

    def test_passenger_signup_missing_fields(self):
        #test missing fields
        missing_fields_data = self.signup_passenger_valid_data.copy()
        missing_fields_data.pop("username")
        missing_fields_data.pop("first_name")

        response = self.client.post(reverse("user_signup", query={'role':'passenger',}), missing_fields_data, follow=True)

        self.assertEqual(response.status_code, 200) # did not redirect
        self.assertFalse(User.objects.filter(username="passenger1").exists()) # user not registered
        form_errors = response.context["form"].errors
        self.assertIn("username", form_errors)
        self.assertEqual(form_errors["username"], ["This field is required."]) # error for missing username
        self.assertEqual(form_errors["first_name"], ["This field is required."]) # error for missing first_name

    def test_passenger_signup_passwords_not_matching(self):
        #test password don't match
        mismatch_passwords_data = self.signup_passenger_valid_data.copy()
        mismatch_passwords_data["password2"] = "NotSoGoodTester2025"

        response = self.client.post(reverse("user_signup", query={'role':'passenger',}), mismatch_passwords_data, follow=True)

        self.assertEqual(response.status_code, 200) # did not redirect
        self.assertFalse(User.objects.filter(username="passenger1").exists()) # user not registered
        form_errors = response.context["form"].errors
        self.assertEqual(form_errors["password2"], ["The two password fields didn’t match."]) # error for passwords not matching


