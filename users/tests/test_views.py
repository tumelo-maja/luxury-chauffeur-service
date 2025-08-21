from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from users.models import Profile, DriverProfile, PassengerProfile


class ProfileViewsPassengerTests(TestCase):
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
        signup_passenger_url = reverse("user_signup", query={'role':'passenger',})
              
        self.client.post(signup_passenger_url, self.signup_passenger_valid_data)
        self.client.login(
            username=self.signup_passenger_valid_data['username'], 
            password=self.signup_passenger_valid_data['password1'])  
                
        self.my_profile_url =reverse("profile",args=[self.signup_passenger_valid_data['username']])


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

        response = self.client.get(reverse("profile-edit")) # navigate back to edit
        self.assertContains(response, "071133445566") #role specific field

    def test_render_profile_settings_view(self):
        #test settings view 
        response = self.client.get(reverse("profile-settings"))
        self.assertContains(response, "Account Settings", status_code=200) 
        self.assertContains(response, "Delete Account") 

    def test_change_email_address_valid_in_profile_settings_view(self):
        #test change email address
        response = self.client.post(reverse("profile-settingschange"), {'email': 'updatedemail@luxtest.com'}, follow=True)  
        self.assertContains(response, "updatedemail@luxtest.com")

    def test_change_email_address_to_other_users_email_invalid_profile_settings_view(self):
        #test change email address to another user's email
        other_user_creds ={
            'username':"other", 
            'email':"otheruseremail@luxtest.com",
            'password':"veryStrongPassword"}
        
        User.objects.create_user(username=other_user_creds["username"],
                                 email=other_user_creds["email"],
                                 password=other_user_creds["password"])
        self.client.logout()
        self.client.login(
            username=self.signup_passenger_valid_data['username'], 
            password=self.signup_passenger_valid_data['password1'])  
        response = self.client.post(reverse("profile-settingschange"), {'email': other_user_creds["email"]}, follow=True)

        self.assertContains(response, f"{other_user_creds["email"]} is already in use.")
        self.assertContains(response, self.signup_passenger_valid_data['username'])# old email still there

    @patch('users.views.send_email_confirmation')
    def test_send_email_confirmation_on_email_address_update(self, mock_send_email):
        # change email
        response = self.client.post(reverse("profile-settingschange"), {'email': 'updatedemail@luxtest.com'})  

        # #check if send_email_confirmation was called once
        user = User.objects.get(username=self.signup_passenger_valid_data['username'])
        mock_send_email.assert_called_once_with(response.wsgi_request, user)

        #check email did change:
        response = self.client.get(reverse("profile-settings"))
        self.assertContains(response, "updatedemail@luxtest.com", status_code=200) 


    @patch('users.views.send_email_confirmation')
    def test_send_email_confirmation_manual_trigger(self, mock_send_email):
        # change email
        response = self.client.get(reverse("profile-emailverify"))

        # check if send_email_confirmation was called once
        user = User.objects.get(username=self.signup_passenger_valid_data['username'])
        mock_send_email.assert_called_once_with(response.wsgi_request, user)

    def test_email_address_confirmation_after_registration(self):
        
        user = User.objects.get(username=self.signup_passenger_valid_data['username'])
        self.email_address = self.email_address = EmailAddress.objects.get(user=user)

        confirmation_key = EmailConfirmationHMAC(self.email_address)
        confirm_email_url = reverse("account_confirm_email", args=[confirmation_key.key])
        print(confirm_email_url)

        response = self.client.post(confirm_email_url)
        self.assertEqual(response.status_code, 302) # should redirect

        self.email_address.refresh_from_db()
        print(self.email_address.verified)
        self.assertTrue(self.email_address.verified)        

    def test_render_account_delete_confirmation_modal(self):
        # initiate account delete
        response = self.client.get(reverse("profile-delete"))

        # check if modal rendered
        self.assertContains(response, "Are you sure you want to delete your account?", status_code=200) 
        self.assertContains(response, "Delete Account") 
