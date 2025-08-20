from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile, DriverProfile, PassengerProfile


class ProfileViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass1234"
        )
        self.client.login(username="testuser", password="pass1234")
        signup_passenger_valid_data= {
            "username": "passenger1",
            "first_name": "Passenger1",
            "last_name": "Tester",
            "email": "passenger1@luxtest.com",
            "password1": "TheUltimateTester2025",
            "password2": "TheUltimateTester2025",
            "role": "passenger",
        } 
        signup_passenger_url = reverse("user_signup", query={'role':'passenger',})
              
        self.client.post(signup_passenger_url, signup_passenger_valid_data)
        self.client.login(
            username=signup_passenger_valid_data['username'], 
            password=signup_passenger_valid_data['password1'])  
                
        self.my_profile_url =reverse("profile",args=[signup_passenger_valid_data['username']])


    def test_profile_uses_correct_template(self):
        response = self.client.get(self.my_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
