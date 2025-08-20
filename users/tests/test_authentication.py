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
        response = self.client.post(self.signup_passenger_url, self.signup_passenger_valid_data, follow=True)

        self.assertTrue(User.objects.filter(username="passenger1").exists()) # is user saved?
        self.assertRedirects(response, reverse("account-success")) # redirected to success page?
        self.assertContains(response, "Please check your inbox to activate your account.", status_code=200) # status=200? text content

    def test_passenger_signup_missing_fields(self):
        #test missing fields
        form_data = self.signup_passenger_valid_data.copy()
        form_data.pop("username")
        form_data.pop("first_name")

        response = self.client.post(self.signup_passenger_url, form_data, follow=True)

        self.assertEqual(response.status_code, 200) # did not redirect
        self.assertFalse(User.objects.filter(username="passenger1").exists()) # user not registered
        form_errors = response.context["form"].errors
        self.assertIn("username", form_errors)
        self.assertEqual(form_errors["username"], ["This field is required."]) # error for missing username
        self.assertEqual(form_errors["first_name"], ["This field is required."]) # error for missing first_name

    def test_passenger_signup_passwords_not_matching(self):
        #test password don't match
        form_data = self.signup_passenger_valid_data.copy()
        form_data["password2"] = "NotSoGoodTester2025"

        response = self.client.post(self.signup_passenger_url, form_data, follow=True)

        self.assertEqual(response.status_code, 200) # did not redirect
        self.assertFalse(User.objects.filter(username="passenger1").exists()) # user not registered
        form_errors = response.context["form"].errors
        self.assertEqual(form_errors["password2"], ["The two password fields didn’t match."]) # error for passwords not matching

    def test_passenger_signup_invalid_email_format(self):
        #test invalid email
        form_data = self.signup_passenger_valid_data.copy()
        form_data["email"] = "passenger1-at-luxtest.com"

        response = self.client.post(self.signup_passenger_url, form_data, follow=True)

        self.assertEqual(response.status_code, 200) # did not redirect
        self.assertFalse(User.objects.filter(username="passenger1").exists()) # user not registered
        form_errors = response.context["form"].errors
        self.assertEqual(form_errors["email"], ["Enter a valid email address."]) # error for passwords not matching

    def test_passenger_signup_duplicate_email_addresses_or_username(self):
        #test duplicate emails
        form_data = self.signup_passenger_valid_data.copy()
        response = self.client.post(self.signup_passenger_url, form_data, follow=True) #first sub,
        self.assertTrue(User.objects.filter(username="passenger1").exists()) # is user saved?
        self.assertRedirects(response, reverse("account-success")) # redirected to success page?

        #duplciate user
        response = self.client.post(self.signup_passenger_url, form_data, follow=True) 

        self.assertEqual(response.status_code, 200) # did not redirect
        form_errors = response.context["form"].errors
        self.assertEqual(form_errors["email"], ["This email is already in use by another user."]) # error duplicate username
        self.assertEqual(form_errors["username"], ["A user with that username already exists."]) # error duplicate email
