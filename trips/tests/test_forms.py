from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import timedelta, datetime
from django.http import Http404
from users.models import Profile, DriverProfile, PassengerProfile, ManagerProfile
from ..models import Trip
from ..forms import *


class TripsFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # password for all
        cls.users_password = "TheUltimateTester2025"
        # create passenger
        cls.user_passenger = User.objects.create_user(
            username="passenger1", password=cls.users_password, email="passenger1@luxtest.com",)
        pass_profile = Profile.objects.get(user=cls.user_passenger)
        pass_profile.user_type = "passenger"
        pass_profile.save()
        cls.profile_passenger = PassengerProfile.objects.create(
            profile=pass_profile)
        cls.profile_passenger.profile.user_type = "passenger"

        # create driver
        cls.user_driver = User.objects.create_user(
            username="driver1", password=cls.users_password, email="driver1@luxtest.com",)
        drive_profile = Profile.objects.get(user=cls.user_driver)
        drive_profile.user_type = "driver"        
        drive_profile.save()
        cls.profile_driver = DriverProfile.objects.create(
            profile=drive_profile)
        cls.profile_driver.profile.user_type = "driver"

        # create manager
        cls.user_manager = User.objects.create_user(
            username="manager1", password=cls.users_password, email="manager1@luxtest.com",)
        man_profile = Profile.objects.get(user=cls.user_manager)
        man_profile.user_type = "manager"        
        man_profile.save()
        cls.profile_manager = ManagerProfile.objects.create(
            profile=man_profile)
        cls.profile_manager.profile.user_type = "manager"

        # url paths
        cls.trips_url = reverse("trips")
        cls.trip_request_url = reverse("trip-request")
        cls.login_url = reverse("account_login")
        cls.login_url = reverse("account_login")
        cls.dash_details_url ='dash-details'
        cls.trip_detail_url = "trip-detail"
        cls.trip_edit_url = "trip-edit"
        cls.trip_cancel_url = "trip-cancel"
        cls.trip_feedback_url = "trip-feedback"
        cls.trip_action_url = "trip-action"
        cls.trip_review_url = "trip-review"
        cls.trip_manager_overview_url = reverse("manager-overview")

        # choice variables
        cls.vehicle_choices = ["Rolls Royce Phantom", "Range Rover Vogue",
                               "Mercedes Benz V-Class", "Premium Limousine", "Classic Vintage Cars",]
        cls.trip_types = ["Airport Transfers", "Special Events",
                          "Corporate Chauffeur", "Private & VIP Chauffeur",]
        
        cls.form_data = {
                    "location_start": "Lux Hotel",
                    "location_end": "Lux International Airport",
                    "travel_datetime": datetime.now()+ timedelta(days=1, hours=2),
                    "driver": cls.profile_driver.id,
                    "vehicle": "Rolls Royce Phantom",
                    "trip_type": "Special Events",
                }


    def login_user(self, user_type):
        self.client.login(
            username=f"{user_type}1",
            password=self.users_password)
        self.user = User.objects.get(username=f"{user_type}1")

    def create_test_trip(self):

        self.client.post(self.trip_request_url, self.form_data)

        self.trip = Trip.objects.get(
            passenger=self.profile_passenger,
            driver=self.profile_driver,
        )          
    
    def test_passenger_can_submit_a_valid_trip_request(self):
        
        self.login_user('passenger')

        response = self.client.post(self.trip_request_url, self.form_data, follow=True)
        self.assertTrue(Trip.objects.filter(passenger=self.profile_passenger).exists())
        self.assertContains(response, "Success! Trip created.",  status_code=200)

    def test_passenger_cannot_submit_a_trip_request_when_required_fields_missing(self):
        
        self.login_user('passenger')

        self.form_data['location_start']=''
        self.form_data['trip_type']=''

        response = self.client.post(self.trip_request_url, self.form_data)

        self.assertFalse(Trip.objects.filter(passenger=self.profile_passenger).exists())

        self.assertFormError(response.context["form"], field='location_start', errors=["This field is required."])
        self.assertFormError(response.context["form"], field='trip_type', errors=["This field is required."])

    def test_passenger_cannot_submit_a_trip_request_for_past_date_or_within_30_minutes(self):
        
        self.login_user('passenger')
        self.form_data['travel_datetime']=datetime.now() - timedelta(days=1, hours=2)

        response = self.client.post(self.trip_request_url, self.form_data)

        self.assertFalse(Trip.objects.filter(passenger=self.profile_passenger).exists())
        self.assertFormError(response.context["form"], field='travel_datetime', errors=["Travel time must be at least 30 minutes from now and not in the past."])

        # check next 15 minutes
        self.form_data['travel_datetime']=datetime.now() + timedelta(minutes=15)
        response = self.client.post(self.trip_request_url, self.form_data)

        self.assertFalse(Trip.objects.filter(passenger=self.profile_passenger).exists())
        self.assertFormError(response.context["form"], field='travel_datetime', errors=["Travel time must be at least 30 minutes from now and not in the past."])

    def test_passenger_cannot_submit_trip_request_within_1_hour_of_another_trip(self):
        
        self.login_user('passenger')
        #trip 1
        self.form_data['travel_datetime']=datetime.now() + timedelta(days=1, hours=2)
        response = self.client.post(self.trip_request_url, self.form_data)
        self.assertEqual(Trip.objects.filter(passenger=self.profile_passenger).count(),1)

        #trip 2 -fail
        self.form_data['travel_datetime']=datetime.now() + timedelta(days=1, hours=1)
        response = self.client.post(self.trip_request_url, self.form_data)
        self.assertFormError(response.context["form"], field='travel_datetime', errors=["You already have another trip scheduled within 1 hour of this time."])
        self.assertEqual(Trip.objects.filter(passenger=self.profile_passenger).count(),1)

        #trip 3 - success
        self.form_data['travel_datetime']=datetime.now() + timedelta(days=1, hours=5)
        response = self.client.post(self.trip_request_url, self.form_data)
        self.assertEqual(Trip.objects.filter(passenger=self.profile_passenger).count(),2)

    def test_passenger_can_edit_existing_trip_changing_its_status_changes_to_modified(self):
        
        self.login_user('passenger')
    
        self.create_test_trip()
        self.assertEqual(self.trip.status,'pending')
        self.assertEqual(self.trip.vehicle,"Rolls Royce Phantom")
        self.assertEqual(self.trip.trip_type,"Special Events")

        #modify form data
        self.form_data['vehicle'] = "Mercedes Benz V-Class"
        self.form_data['trip_type'] = "Private & VIP Chauffeur"

        # post form
        response = self.client.post(reverse(self.trip_edit_url, args=[self.trip.trip_name]),self.form_data, follow=True)
        self.assertContains(response, "Success! Trip modified.",  status_code=200)
        self.trip.refresh_from_db()

        self.assertEqual(self.trip.status,'modified')
        self.assertEqual(self.trip.vehicle,"Mercedes Benz V-Class")
        self.assertEqual(self.trip.trip_type,"Private & VIP Chauffeur")        

    def test_passenger_can_cancel_existing_trip_changing_its_status_changes_to_cancelled(self):
        
        self.login_user('passenger')
    
        self.create_test_trip()
        self.assertEqual(self.trip.status,'pending')

        # post form
        response = self.client.post(reverse(self.trip_cancel_url, args=[self.trip.trip_name]), follow=True)
        self.assertContains(response, "Success! Trip cancelled.",  status_code=200)
        self.trip.refresh_from_db()

        self.assertEqual(self.trip.status,'cancelled')

    def test_driver_can_start_a_confirmed_trip_changing_its_status_changes_to_in_progress(self):
        
        self.login_user('passenger')
    
        self.create_test_trip()
        self.trip.status='confirmed'        
        self.trip.save()
        self.assertEqual(self.trip.status,'confirmed')

        # post form
        # as passenger
        response = self.client.post(reverse(self.trip_action_url, args=[self.trip.trip_name]), follow=True)
        self.assertContains(response, "You are not authorized to access this resource",  status_code=200)

        self.client.logout()
        self.login_user('driver')
        response = self.client.post(reverse(self.trip_action_url, args=[self.trip.trip_name]), follow=True)
        self.assertContains(response, "Success! Trip started.",  status_code=200)
        self.trip.refresh_from_db()

        self.assertEqual(self.trip.status,'in_progress')        


    def test_driver_can_end_a_trip_in_progress_changing_its_status_changes_to_completed(self):
        
        self.login_user('passenger')
    
        self.create_test_trip()
        self.trip.status='in_progress'        
        self.trip.save()
        self.assertEqual(self.trip.status,'in_progress')

        # post form
        self.client.logout()
        self.login_user('driver')
        response = self.client.post(reverse(self.trip_action_url, args=[self.trip.trip_name]), follow=True)
        self.assertContains(response, "Success! Trip ended.",  status_code=200)


        self.trip.refresh_from_db()
        self.assertEqual(self.trip.status,'completed')    

    def test_manager_can_approve_or_reject_a_pending_or_modified_trip_changing_its_status_changes_to_confirmed(self):
        
        self.login_user('passenger')
        self.create_test_trip()

        # pending
        self.client.logout()
        self.login_user('manager')
        self.trip.status='pending'        
        self.trip.save()
        response = self.client.post(reverse(self.trip_review_url, args=[self.trip.trip_name]),{'request_outcome':'approve',}, follow=True)
        self.assertContains(response, "Success! Trip confirmed.",  status_code=200)

        # modified
        self.trip.status='modified'        
        self.trip.save()
        response = self.client.post(reverse(self.trip_review_url, args=[self.trip.trip_name]),{'request_outcome':'reject',}, follow=True)
        self.assertContains(response, "Success! Trip rejected.",  status_code=200)
    

    def test_passenger_or_driver_can_submit_trip_feedback_form_for_completed_trips(self):
        
        self.login_user('passenger')
        self.create_test_trip()
        self.trip.status='completed'        
        self.trip.save()

        form_data ={
            'passenger_rating': 5,
            'passenger_rating_comments': 'Driver was awesome',
        }
        response = self.client.post(reverse(self.trip_feedback_url, args=[self.trip.trip_name]),form_data, follow=True)
        self.assertContains(response, "Success! Trip feedback submitted.",  status_code=200)          


        # driver
        self.client.logout()
        self.login_user('driver')
        form_data ={
            'driver_rating': 3,
            'driver_rating_comments': 'My passenger ok',
        }
        response = self.client.post(reverse(self.trip_feedback_url, args=[self.trip.trip_name]),form_data, follow=True)
        self.assertContains(response, "Success! Trip feedback submitted.",  status_code=200)        


        trips_completed = Trip.objects.filter(status='completed')

        self.profile_passenger.update_rating(trips_completed)
        self.profile_driver.update_rating(trips_completed)
   
 
        self.assertEqual(self.profile_passenger.average_rating,3.0) 
        self.assertEqual(self.profile_driver.average_rating,5.0) 


