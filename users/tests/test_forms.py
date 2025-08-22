from django.test import TestCase 
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.models import User
from ..models import Profile, DriverProfile, PassengerProfile, ManagerProfile

class UsersFormsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.signup_type_url = reverse("signup_type")
        cls.signup_driver_url = reverse("user_signup", query={'role':'driver',})
        cls.signup_passenger_url = reverse("user_signup", query={'role':'passenger',})

        cls.login_url = reverse("account_login")
        cls.logout_url = reverse("account_logout")

        cls.user_form_data= {
            "username": "testuser1",
            "first_name": "testuser1",
            "last_name": "Tester",
            "email": "testuser1@luxtest.com",
            "password1": "TheUltimateTester2025",
            "password2": "TheUltimateTester2025",
            "role": "passenger",
        }

        cls.login_user_valid_data ={
            "username": "testuser1",
            "email": "testuser1@luxtest.com",
            "password": "TheUltimateTester2025",            
        }

        cls.my_profile_url =reverse("profile",args=[cls.login_user_valid_data['username']])
        cls.profile_delete_url = reverse("profile-delete")

    def register_user(self, user_type):
        if user_type == 'passenger':
            role_form_data = self.user_form_data
            role_form_data['role']= user_type
            return self.client.post(self.signup_passenger_url, role_form_data)
        elif user_type == 'driver':
            role_form_data = self.user_form_data
            role_form_data['role']= user_type
            return self.client.post(self.signup_driver_url, role_form_data)
        
    def login_user(self):
        self.client.login(
            username=self.login_user_valid_data['username'], 
            password=self.login_user_valid_data['password'])

    def authenticate_user(self, user_type):
        self.register_user(user_type)
        self.login_user()
        self.user = User.objects.get(username=self.user_form_data['username'])    
        self.profile = Profile.objects.get(user=self.user)
    
    def authenticate_manager(self):
        self.user = User.objects.create_user(username=self.user_form_data['username'], password=self.user_form_data['password1'])
        self.profile = Profile.objects.get(user=self.user)
        self.manager_profile = ManagerProfile.objects.create(profile=self.profile)
        self.login_user()

        
    def test_user_account_created_when_submitting_valid_form(self):
        #test signup for passenger 
        response = self.client.post(self.signup_passenger_url, self.user_form_data, follow=True)

        self.assertTrue(User.objects.filter(username="testuser1").exists()) # is user saved?
        self.assertRedirects(response, reverse("account-success")) # redirected to success page?
        self.assertContains(response, "Please check your inbox to activate your account.", status_code=200) # status=200? text content

    def test_profile_created_when_user_account_created(self):
        #test profile created
        self.client.post(self.signup_passenger_url, self.user_form_data, follow=True)
        user = User.objects.get(username="testuser1")
        self.assertTrue(Profile.objects.filter(user=user).exists()) 

    def test_passengerprofile_created_when_user_and_profile_are_created_using_passenger_link(self):
        #test passengerprofile created
        self.client.post(self.signup_passenger_url, self.user_form_data, follow=True)
        user = User.objects.get(username="testuser1")
        self.assertEqual(user.profile.user_type,'passenger') 
        self.assertTrue(PassengerProfile.objects.filter(profile=user.profile).exists()) 

    def test_driverprofile_created_when_user_and_profile_are_created_using_driver_link(self):
        #test passengerprofile created
        self.user_form_data['role']='driver'
        self.client.post(self.signup_driver_url, self.user_form_data, follow=True)
        user = User.objects.get(username="testuser1")
        self.assertEqual(user.profile.user_type,'driver') 
        self.assertTrue(DriverProfile.objects.filter(profile=user.profile).exists()) 

    def test_passenger_user_not_created_when_submitting_form_with_missing_fields(self):
        #test missing fields
        form_data = self.user_form_data.copy()
        form_data.pop("username")
        form_data.pop("first_name")

        response = self.client.post(self.signup_passenger_url, form_data, follow=True)

        self.assertEqual(response.status_code, 200) # did not redirect
        self.assertFalse(User.objects.filter(username="testuser1").exists()) # user not registered
        form_errors = response.context["form"].errors
        self.assertIn("username", form_errors)
        self.assertEqual(form_errors["username"], ["This field is required."]) # error for missing username
        self.assertEqual(form_errors["first_name"], ["This field is required."]) # error for missing first_name

    def test_passenger_user_not_created_when_passwords_dont_match(self):
        #test password don't match
        form_data = self.user_form_data.copy()
        form_data["password2"] = "NotSoGoodTester2025"

        response = self.client.post(self.signup_passenger_url, form_data, follow=True)

        self.assertEqual(response.status_code, 200) # did not redirect
        self.assertFalse(User.objects.filter(username="testuser1").exists()) # user not registered
        form_errors = response.context["form"].errors
        self.assertEqual(form_errors["password2"], ["The two password fields didn’t match."]) # error for passwords not matching

    def test_passenger_user_not_created_when_invalid_email_format_entered(self):
        #test invalid email
        form_data = self.user_form_data.copy()
        form_data["email"] = "testuser1-at-luxtest.com"

        response = self.client.post(self.signup_passenger_url, form_data, follow=True)

        self.assertEqual(response.status_code, 200) # did not redirect
        self.assertFalse(User.objects.filter(username="testuser1").exists()) # user not registered
        form_errors = response.context["form"].errors
        self.assertEqual(form_errors["email"], ["Enter a valid email address."]) # error for passwords not matching

    def test_passenger_user_not_created_when_signup_email_already_exist(self):
        #test duplicate emails
        form_data = self.user_form_data.copy()
        response = self.client.post(self.signup_passenger_url, form_data, follow=True) #first sub,
        self.assertTrue(User.objects.filter(username="testuser1").exists()) # is user saved?
        self.assertRedirects(response, reverse("account-success")) # redirected to success page?

        #duplciate user
        response = self.client.post(self.signup_passenger_url, form_data, follow=True) 

        self.assertEqual(response.status_code, 200) # did not redirect
        form_errors = response.context["form"].errors
        self.assertEqual(form_errors["email"], ["This email is already in use by another user."]) # error duplicate username
        self.assertEqual(form_errors["username"], ["A user with that username already exists."]) # error duplicate email


    def test_successful_login_when_valid_email_is_passed(self):
        #test email valid login
        self.register_user('passenger')
        self.client.login(
            email=self.login_user_valid_data['email'], 
            password=self.login_user_valid_data['password'])

        #test 'My profile view'
        response = self.client.get(self.my_profile_url)
        self.assertContains(response, "Edit Profile", status_code=200) # status=200? text content

    def test_successful_login_when_valid_username_is_passed(self):
        #test username valid login
        self.register_user('passenger')
        self.client.login(
            username=self.login_user_valid_data['username'], 
            password=self.login_user_valid_data['password'])

        #test 'My profile view'
        response = self.client.get(self.my_profile_url)
        self.assertContains(response, "Edit Profile", status_code=200) # status=200? text content 

    def test_unsuccessful_login_when_incorrect_password_is_passed(self):
        #test username valid login
        self.register_user('passenger')

        #wrong password
        response = self.client.post(self.login_url, {
            "login":self.login_user_valid_data['email'], 
            "password":self.login_user_valid_data['password']+"wrong"
            })
        self.assertContains(response, "The email address and/or password you specified are not correct.", status_code=200) # check wrong password

    def test_unsuccessful_login_when_incorrect_email_is_passed(self):
        #test username valid login
        self.register_user('passenger')

        # wrong email
        response = self.client.post(self.login_url, {
            "login":'wrongemail@luxtest.com', 
            "password":self.login_user_valid_data['password']
            })
        self.assertContains(response, "The email address and/or password you specified are not correct.", status_code=200) # check wrong email

    def test_unsuccessful_login_when_incorrect_username_is_passed(self):
        #test username valid login
        self.register_user('passenger')

        # wrong username
        response = self.client.post(self.login_url, {
            "login": 'wrongusername', 
            "password":self.login_user_valid_data['password']
            })
        self.assertContains(response, "The username and/or password you specified are not correct.", status_code=200) # check wrong username

    def test_successful_passenger_logout(self):
        #test logout
        self.register_user('passenger')
        self.login_user()

        #check user is logged in 
        response = self.client.get(self.my_profile_url)
        self.assertContains(response, "Edit Profile", status_code=200) 

        #logout user
        self.client.logout()

        #check if redirected to login page
        response = self.client.get(self.my_profile_url)
        self.assertRedirects(response, expected_url=f"{self.login_url}?next={self.my_profile_url}")
        

    @patch('users.views.send_email_confirmation')
    def test_email_confirmation_sent_to_user_on_user_registration(self, mock_send_email):
        response =self.register_user('passenger')

        # #check if send_email_confirmation was called once
        user = User.objects.get(username=self.login_user_valid_data['username'])
        mock_send_email.assert_called_once_with(response.wsgi_request, user)


    def test_render_account_delete_confirmation_modal(self):
        # initiate account delete
        self.authenticate_user('passenger')
        response = self.client.get(self.profile_delete_url)

        # check if modal rendered
        self.assertContains(response, "Are you sure you want to delete your account?", status_code=200) 
        self.assertContains(response, "Delete Account") 

    def test_user_account_deleted_after_confirming_account_delete(self):
        # initiate account delete
        self.authenticate_user('passenger')
        response = self.client.post(self.profile_delete_url, follow=True)
        print(response)
        # check if goodbye message rendered
        self.assertContains(response, "Account deleted! See you next time", status_code=200) 
        # check if has been deleted
        self.assertFalse(User.objects.filter(username=self.user_form_data['username']).exists())

    def test_profile_deleted_on_user_account_delete(self):
        self.authenticate_user('passenger')

        self.assertTrue(User.objects.filter(username="testuser1").exists()) 
        self.assertTrue(Profile.objects.filter(user=self.user).exists()) 

        self.client.post(self.profile_delete_url, follow=True)

        self.assertFalse(User.objects.filter(username="testuser1").exists()) 
        self.assertFalse(Profile.objects.filter(user=self.user).exists())
        

    def test_passengerprofile_deleted_on_profile_delete(self):
        self.authenticate_user('passenger')

        self.assertTrue(Profile.objects.filter(user=self.user).exists()) 
        self.assertTrue(PassengerProfile.objects.filter(profile=self.profile).exists()) 

        self.client.post(self.profile_delete_url, follow=True)

        self.assertFalse(Profile.objects.filter(user=self.user).exists()) 
        self.assertFalse(PassengerProfile.objects.filter(profile=self.profile).exists()) 

    def test_driverprofile_deleted_on_profile_delete(self):
        self.authenticate_user('driver')

        self.assertTrue(Profile.objects.filter(user=self.user).exists()) 
        self.assertTrue(DriverProfile.objects.filter(profile=self.profile).exists()) 

        self.client.post(self.profile_delete_url, follow=True)

        self.assertFalse(Profile.objects.filter(user=self.user).exists()) 
        self.assertFalse(DriverProfile.objects.filter(profile=self.profile).exists()) 

    def test_managerprofile_deleted_on_profile_delete(self):
        self.authenticate_manager()

        self.assertTrue(Profile.objects.filter(user=self.user).exists()) 
        self.assertTrue(ManagerProfile.objects.filter(profile=self.profile).exists()) 

        self.client.post(self.profile_delete_url, follow=True)

        self.assertFalse(Profile.objects.filter(user=self.user).exists()) 
        self.assertFalse(ManagerProfile.objects.filter(profile=self.profile).exists()) 
