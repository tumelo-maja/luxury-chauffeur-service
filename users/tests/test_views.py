from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile, DriverProfile, PassengerProfile


class ProfileViewsPassengerTests(TestCase):
    def setUp(self):

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
        #test template rendered
        response = self.client.get(self.my_profile_url)
        self.assertContains(response, "Edit Profile", status_code=200) 
        self.assertTemplateUsed(response, "users/profile.html")
    
    def test_render_profile_edit_passenger_view(self):
        #test edit view 
        response = self.client.get(reverse("profile-edit"))
        self.assertContains(response, "Edit your Profile", status_code=200) 
        self.assertContains(response, "Passenger Information") 

    def test_update_passenger_profile_on_profile_edit_view(self):
        #test edit view 
        # response = self.client.get(reverse("profile-edit"))
        form_data ={
            "displayname": "The Highest",
            "title": "Lord",
            "phone": "07999112231",
            "home_address": "20 Oxford Street, London",
            "emergency_name": "Kim EC",
            "emergency_phone": "071133445566",                     
        }
        response = self.client.post(reverse("profile-edit"), form_data, follow=True)        
        self.assertContains(response, "The Highest", status_code=200) 
        self.assertContains(response, "20 Oxford Street, London") 

        response = self.client.get(reverse("profile-edit"))
        self.assertContains(response, "071133445566") #role specific form

    def test_render_profile_settings_view(self):
        #test edit view 
        response = self.client.get(reverse("profile-settings"))
        self.assertContains(response, "Account Settings", status_code=200) 
        self.assertContains(response, "Delete Account") 

