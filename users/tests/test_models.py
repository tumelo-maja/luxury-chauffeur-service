from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from users.models import Profile, DriverProfile, PassengerProfile, ManagerProfile

class UsersProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="passenger1", password="TheUltimateTester2025")
        cls.profile = Profile.objects.get(user=cls.user)

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

    def test_avatar_property_returns_static_image_if_no_cloudinary_url_image(self):
  
        self.assertIn('placeholder', self.profile.image.public_id)
        self.assertIn('avatar.png', self.profile.avatar)

    def test_avatar_property_returns_cloudinary_url_image_if_exists(self):
        # creta dummy image object
        test_image = MagicMock()
        test_image.public_id = "real_image"
        test_image.url = "https://lux.com/image-for-testing.jpg"
        self.profile.image = test_image

        self.assertEqual(self.profile.avatar, "https://lux.com/image-for-testing.jpg")
    

class UsersPassengerProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="passenger1", password="TheUltimateTester2025")
        self.profile = Profile.objects.get(user=self.user)
        self.profile.user_type="passenger"
        self.passenger_profile = PassengerProfile.objects.create(profile=self.profile)
    
    def test_str_returns_passenger_username(self):
        self.assertEqual(str(self.passenger_profile),"Passenger: passenger1")
    
    def test_profile_status_matches_passenger_profile_status(self):
        self.assertEqual(self.profile.status,self.passenger_profile.status)


class UsersDriverProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="driver1", password="TheUltimateTester2025")
        self.profile = Profile.objects.get(user=self.user)
        self.profile.user_type="driver"
        self.driver_profile = DriverProfile.objects.create(profile=self.profile)
    
    def test_str_returns_driver_username(self):
        self.assertEqual(str(self.driver_profile),"Driver: driver1")
    
    def test_profile_status_matches_driver_profile_status(self):
        self.assertEqual(self.profile.status,self.driver_profile.status)

class UsersManagerProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="manager1", password="TheUltimateTester2025")
        self.profile = Profile.objects.get(user=self.user)
        self.profile.user_type="manager"
        self.manager_profile = ManagerProfile.objects.create(profile=self.profile)
    
    def test_str_returns_manager_username(self):
        self.assertEqual(str(self.manager_profile),"Manager: manager1")
    
    def test_profile_status_matches_manager_profile_status(self):
        self.assertEqual(self.profile.status,self.manager_profile.status)