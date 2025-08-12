from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from cloudinary.models import CloudinaryField

TITLE_OPTIONS = [
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Ms', 'Ms'),
    ('Dr', 'Dr'),
    ('Prof', 'Prof'),
    ('Lord', 'Lord'),
    ('Sir', 'Sir'),
]
USER_TYPE_CHOICES = [
    ('driver', 'Driver'),
    ('passenger', 'Passenger'),
    ('manager', 'Manager'),
]


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='passenger')

    # image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    image = CloudinaryField('image', default='placeholder')
    displayname = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(
        max_length=20, choices=TITLE_OPTIONS, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    home_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    @property
    def name(self):
        if self.displayname:
            name = self.displayname
        else:
            name = self.user.username
        return name

    @property
    def avatar(self):
        try:
            avatar = self.image.url
            if avatar is None:
                raise TypeError
        except:
            avatar = static('images/avatar.png')
        return avatar


class PassengerProfile(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='passenger_profile')
    emergency_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=15)
    average_rating = models.FloatField(null=True, blank=True)
    count_rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Passenger: {self.profile.user.username}"


    def update_rating(self,trips):
        if trips.exists():
            rating_items = [trip.driver_rating for trip in trips if trip.driver_rating is not None]
            self.count_rating = len(rating_items)
            self.average_rating = sum(rating_items) / len(rating_items)
            self.save()

    def get_rating_levels(self,trips):
        
        rating_counts = {f'star_{i}': 0 for i in range(1, 6)}
        for trip in trips:
            rating = trip.driver_rating

            if f'star_{rating}' in rating_counts:
                rating_counts[f'star_{rating}'] += 1

        return rating_counts


class DriverProfile(models.Model):

    DRIVER_STATUS_OPTIONS = [
        ('available', 'Available'),
        ('engaged', 'Engaged'),
        ('unavailable', 'Unavailable'),
    ]
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='driver_profile')
    experience = models.IntegerField(default=2)

    status = models.CharField(
        max_length=50, choices=DRIVER_STATUS_OPTIONS, default="available")
    average_rating = models.FloatField(null=True, blank=True)
    count_rating = models.IntegerField(null=True, blank=True)
    count_rating2 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Driver: {self.profile.user.username}"
    
    def update_status(self, status):
        self.status = status
        self.save()
    
    
    def update_rating(self,trips):
        if trips.exists():
            rating_items = [trip.passenger_rating for trip in trips if trip.passenger_rating is not None]
            self.count_rating = len(rating_items)
            self.average_rating = sum(rating_items) / len(rating_items)
            self.save()

    def get_rating_levels(self,trips):
        
        rating_counts = {f'star_{i}': 0 for i in range(1, 6)}
        for trip in trips:
            rating = trip.passenger_rating

            if f'star_{rating}' in rating_counts:
                rating_counts[f'star_{rating}'] += 1

        return rating_counts

class ManagerProfile(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='manager_profile')

    experience = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"Manager: {self.profile.user.username}"

    def update_rating(self,trips):
        if trips.exists():
            passenger_rating_items = [trip.passenger_rating for trip in trips if trip.passenger_rating is not None]
            self.passenger_count_rating = len(passenger_rating_items)
            self.passenger_average_rating = sum(passenger_rating_items) / len(passenger_rating_items)

            driver_rating_items = [trip.driver_rating for trip in trips if trip.driver_rating is not None]
            self.driver_count_rating = len(driver_rating_items)
            self.driver_average_rating = sum(driver_rating_items) / len(driver_rating_items)

            self.save()

    def get_rating_levels(self,trips):
        
        rating_counts = {f'star_{i}': 0 for i in range(1, 6)}
        for trip in trips:
            rating = trip.passenger_rating

            if f'star_{rating}' in rating_counts:
                rating_counts[f'star_{rating}'] += 1

        return rating_counts