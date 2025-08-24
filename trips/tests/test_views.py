from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from django.http import Http404
from users.models import Profile, DriverProfile, PassengerProfile, ManagerProfile
from ..models import Trip


class TripsViewTest(TestCase):

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
        cls.dash_details_url ='dash-details'
        cls.trip_detail_url = "trip-detail"
        cls.trip_edit_url = "trip-edit"
        cls.trip_cancel_url = "trip-cancel"
        cls.trip_feedback_url = "trip-feedback"
        cls.trip_action_url = "trip-action"
        cls.trip_review_url = "trip-review"

        # choice variables
        cls.vehicle_choices = ["Rolls Royce Phantom", "Range Rover Vogue",
                               "Mercedes Benz V-Class", "Premium Limousine", "Classic Vintage Cars",]
        cls.trip_types = ["Airport Transfers", "Special Events",
                          "Corporate Chauffeur", "Private & VIP Chauffeur",]

    def login_user(self, user_type):
        self.client.login(
            username=f"{user_type}1",
            password=self.users_password)
        self.user = User.objects.get(username=f"{user_type}1")
    
    def login_other_passenger(self, user_type):
        self.user_passenger_other = User.objects.create_user(
        username=f"{user_type}_other1", password=self.users_password, email=f"{user_type}_other1@luxtest.com",)
        user_profile = Profile.objects.get(user=self.user_passenger_other)
        user_profile.user_type = user_type
        user_profile.save()
        
        if user_type == "passenger":
            self.profile_passenger_other = PassengerProfile.objects.create(
            profile=user_profile)
            self.profile_passenger_other.profile.user_type = user_type
        elif user_type == "driver":
            self.profile_driver_other = DriverProfile.objects.create(
            profile=user_profile)
            self.profile_driver_other.profile.user_type = user_type            
        self.login_user(f'{user_type}_other')
    
    def create_test_trip(self):

        self.trip = Trip.objects.create(
            passenger=self.profile_passenger,
            driver=self.profile_driver,
            location_start='Lux Hotel',
            location_end='Lux Aiport',
            travel_datetime=parse_datetime("2025-09-21T15:30:00Z"),
            trip_type="Airport Transfers",
            vehicle="Range Rover Vogue",
        )     
   
    
    def test_unauthenticated_users_are_redirected_to_login_when_accessing_trips_page(self):
        response = self.client.get(self.trips_url)
        self.assertRedirects(response, expected_url=f"{self.login_url}?next={self.trips_url}")

    def test_authenticated_users_can_access_trips_page(self):
        self.login_user('passenger')
        response = self.client.get(self.trips_url)
        self.assertContains(response, "Manage your trips with ease.", status_code=200) 

    def test_trips_page_uses_correct_template(self):
        #test template rendered
        self.login_user('passenger')
        response = self.client.get(self.trips_url)
        self.assertTemplateUsed(response, "trips/trips.html")

    def test_correct_headings_are_rendered_in_trips_summary_view(self):
        #test template rendered
        self.login_user('passenger')
        response = self.client.get(reverse(self.dash_details_url,args=['home']))
        self.assertContains(response, "Trips Summary") 
        self.assertContains(response, "Ratings") 
        self.assertContains(response, "Recent Activities") 

    def test_trips_list_view_rendered_correctly(self):
        #test template rendered
        self.login_user('passenger')
        response = self.client.get(reverse(self.dash_details_url,args=['list-view']))
        self.assertContains(response, "My trips") 

    def test_trips_calendar_view_rendered_correctly(self):
        #test template rendered
        self.login_user('passenger')
        response = self.client.get(reverse(self.dash_details_url,args=['calendar-view']))
        self.assertContains(response, "userCalendar") 
        self.assertContains(response, "Wed")

    def test_no_trips_rendered_if_no_trips_created(self):

        self.login_user('passenger')
        response = self.client.get(reverse(self.dash_details_url,args=['home']))
        self.assertContains(response, '<span id="total-trips">0</span>') 

        response = self.client.get(reverse(self.dash_details_url,args=['list-view']))
        self.assertContains(response, 'You do not have any trips.') 

    def test_trips_rendered_in_the_trips_page_when_available(self):

        self.login_user('passenger')
        self.assertFalse(Trip.objects.filter(passenger=self.profile_passenger).exists())  # no trips

        self.create_test_trip()
        self.trip.refresh_from_db()

        self.assertTrue(Trip.objects.filter(passenger=self.profile_passenger).exists())  # 1 trip
        response = self.client.get(reverse(self.dash_details_url,args=['home']))
        self.assertContains(response, '<span id="total-trips">1</span>') 

        response = self.client.get(reverse(self.dash_details_url,args=['list-view']))
        self.assertContains(response, self.trip.trip_name)         


    def test_passenger_user_can_launch_trip_request_modal(self):

        self.login_user('passenger')
        response = self.client.get(self.trip_request_url)

        self.assertContains(response, 'Enter pickup location...')        
        self.assertContains(response, 'csrfmiddlewaretoken')        
        self.assertContains(response, 'type="submit"')        

    def test_non_passenger_users_cannot_launch_trip_request_modal(self):

        self.login_user('driver')
        response = self.client.get(self.trip_request_url)

        self.assertContains(response, 'Action not allowed') 
        self.client.logout()

        self.login_user('manager')
        response = self.client.get(self.trip_request_url)

        self.assertContains(response, 'Action not allowed') 

    def test_passenger_user_can_veiw_trip_details_of_own_trips(self):

        self.login_user('passenger')
        self.create_test_trip()
        response = self.client.get(reverse(self.trip_detail_url,args=[self.trip.trip_name]))

        self.assertContains(response, 'trip-detail-container')        
        self.assertContains(response, 'Edit Trip')        
        self.assertContains(response, 'Cancel Trip')              

    def test_passenger_user_cannot_veiw_trip_details_of_other_passengers(self):

        self.create_test_trip()

        self.login_other_passenger('passenger')
        response = self.client.get(reverse(self.trip_detail_url,args=[self.trip.trip_name]))
        self.assertContains(response, "Error 404: This resource doesn't exist or is unavailable",status_code=404)        

    def test_passenger_user_can_launch_edit_modal_for_trips_not_reject_cancelled_inprogress_or_completed(self):

        self.login_user('passenger')
        self.create_test_trip()

        editable_status = ["in_progress", "cancelled","completed","rejected"]
        for status in editable_status:
            self.trip.status=status
            response = self.client.get(reverse(self.trip_edit_url,args=[self.trip.trip_name]))

            self.assertContains(response, 'Lux Aiport')        
            self.assertContains(response, 'Save Changes')

    def test_passenger_user_can_launch_cancel_modal_for_trips_not_reject_cancelled_inprogress_or_completed(self):

        self.login_user('passenger')
        self.create_test_trip()
        response = self.client.get(reverse(self.trip_cancel_url,args=[self.trip.trip_name]))
        self.assertContains(response, 'Warning! You are about to cancel the Trip:')        
        self.assertContains(response, 'Yes, Cancel Trip')       

    def test_passenger_and_driver_users_can_launch_feedback_modal_for_completed_trips(self):

        self.login_user('passenger')
        self.create_test_trip()
        self.trip.status='completed'
        response = self.client.get(reverse(self.trip_feedback_url,args=[self.trip.trip_name]))
        self.assertContains(response, f'How was your experience with {self.profile_driver.profile.name} on this trip?')        
        self.assertContains(response, 'Rate your Chauffeur')
        self.client.logout()

        self.login_user('driver')
        response = self.client.get(reverse(self.trip_feedback_url,args=[self.trip.trip_name]))
        self.assertContains(response, f'How was your experience with {self.profile_passenger.profile.name} on this trip?')        
        self.assertContains(response, 'Rate your Passenger')

     
                   
    def test_only_driver_assigned_to_trip_can_access_trip_action_for_confirmed_or_inprogress_trips(self):

        self.create_test_trip()

        self.login_user('driver')
        # trip status 'pending' after creation
        response = self.client.get(reverse(self.trip_action_url,args=[self.trip.trip_name]))
        self.assertContains(response, f"This action is not allowed for trip with status: {self.trip.status}")           

        # change trip status to 'confirmed'
        self.trip.status='confirmed'
        self.trip.save()
        response = self.client.get(reverse(self.trip_action_url,args=[self.trip.trip_name]))
        self.assertContains(response, "Start Trip")

        # change trip status to 'in_progress'
        self.trip.status='in_progress'
        self.trip.save()
        response = self.client.get(reverse(self.trip_action_url,args=[self.trip.trip_name]))
        self.assertContains(response, "End Trip")        

        #check for other drivers
        self.client.logout()
        self.login_other_passenger('driver')
        response = self.client.get(reverse(self.trip_action_url,args=[self.trip.trip_name]))
        self.assertContains(response, "Error 404: This resource doesn't exist or is unavailable",status_code=404)  

    def test_only_manager_user_can_access_trip_review_to_approve_or_reject_trips(self):

        self.create_test_trip()

        self.login_user('manager')
        response = self.client.get(reverse(self.trip_review_url,args=[self.trip.trip_name]))
        self.assertContains(response, "Review Trip")    

        #check for drivers
        self.client.logout()
        self.login_user('driver')
        response = self.client.get(reverse(self.trip_review_url,args=[self.trip.trip_name]))
        self.assertContains(response, "Error 404: This resource doesn't exist or is unavailable",status_code=404)

        #check for passenger
        self.client.logout()
        self.login_user('passenger')
        response = self.client.get(reverse(self.trip_review_url,args=[self.trip.trip_name]))
        self.assertContains(response, "Error 404: This resource doesn't exist or is unavailable",status_code=404)                  