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
    
    def create_other_passenger(self):
        self.user_passenger_other = User.objects.create_user(
        username="passenger_other1", password=self.users_password, email="passenger_other1@luxtest.com",)
        pass_profile = Profile.objects.get(user=self.user_passenger_other)
        pass_profile.user_type = "passenger"
        pass_profile.save()
        self.profile_passenger_other = PassengerProfile.objects.create(
        profile=pass_profile)
        self.profile_passenger_other.profile.user_type = "passenger"
    
    def create_test_trip(self,pick_up,drop_off,trip_date):
        self.trip = Trip.objects.create(
            passenger=self.profile_passenger,
            driver=self.profile_driver,
            location_start=pick_up,
            location_end=drop_off,
            travel_datetime=parse_datetime(trip_date),
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

        self.create_test_trip('Lux Hotel','Lux Aiport',"2025-09-21T15:30:00Z")
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
        self.create_test_trip('Lux Hotel','Lux Aiport',"2025-09-21T15:30:00Z")
        response = self.client.get(reverse(self.trip_detail_url,args=[self.trip.trip_name]))

        self.assertContains(response, 'trip-detail-container')        
        self.assertContains(response, 'Edit Trip')        
        self.assertContains(response, 'Cancel Trip')              

    def test_passenger_user_cannot_veiw_trip_details_of_other_passengers(self):

        self.login_user('passenger')
        self.create_test_trip('Lux Hotel','Lux Aiport',"2025-09-21T15:30:00Z")
        self.client.logout()

        self.create_other_passenger()
        self.login_user('passenger_other')
        response = self.client.get(reverse(self.trip_detail_url,args=[self.trip.trip_name]))
        self.assertContains(response, "Error 404: This resource doesn't exist or is unavailable",status_code=404)        

    def test_passenger_user_can_launch_trip_edit_modal_for_existing_tip(self):

        self.login_user('passenger')
        self.create_test_trip('Lux Hotel','Lux Aiport',"2025-09-21T15:30:00Z")
        response = self.client.get(reverse(self.trip_edit_url,args=[self.trip.trip_name]))

        self.assertContains(response, 'Lux Aiport')        
        self.assertContains(response, 'Save Changes')

    def test_passenger_user_can_launch_trip_cancel_modal_for_existing_tip(self):

        self.login_user('passenger')
        self.create_test_trip('Lux Hotel','Lux Aiport',"2025-09-21T15:30:00Z")
        response = self.client.get(reverse(self.trip_cancel_url,args=[self.trip.trip_name]))
        print(response.content)
        self.assertContains(response, 'Warning! You are about to cancel the Trip:')        
        self.assertContains(response, 'Yes, Cancel Trip')       
