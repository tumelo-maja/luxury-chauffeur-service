"""
User app models.

Handles data models definitions related to user accounts and profiles.

"""
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from cloudinary.models import CloudinaryField
from django.contrib import admin

USER_STATUS_OPTIONS = [
    ('available', 'Available'),
    ('engaged', 'Engaged'),
    ('unavailable', 'Unavailable'),
]


class Profile(models.Model):
    """
    Extends the Django User model.

    Stores generic user details used across different role specific profiles.
    """

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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='passenger')
    image = CloudinaryField('image', default='placeholder')
    displayname = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(
        max_length=20, choices=TITLE_OPTIONS, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    home_address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=USER_STATUS_OPTIONS, default="available")

    def __str__(self):
        return f"{self.user}"

    @property
    def name(self):
        """
        Set Display name if specified by user else the username is returned.
        """
        if self.displayname:
            name = self.displayname
        else:
            name = self.user.username
        return name

    @property
    def avatar(self):
        """
        Set user avatar to the cloudinary url if user added an image else the default user avatar in static folder is used .
        """
        try:
            # avatar = self.image.url
            # if avatar is None:
            #     raise TypeError
            if self.image and self.image.public_id != "placeholder":
                return self.image.url
            raise ValueError
        except:
            avatar = static('images/avatar.png')
        return avatar

    def update_status(self, status):
        """
        Updates the status field with value specified by `status` argument  then saves.
        """
        self.status = status
        self.save()


class PassengerProfile(models.Model):
    """
    Passenger role-specific profile.
    Related to `Profile` model by one-to-one relationship.

    Stores emergency contact information and ratings received from user's completed trips.
    """
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='passenger_profile')
    emergency_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=15)
    average_rating = models.FloatField(default=0.0)
    count_rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Passenger: {self.profile.user.username}"

    @property
    @admin.display(ordering="profile")
    def status(self):
        return self.profile.status
    
    def update_rating(self, trips):
        """
        Update passenger's rating statistics.

        `count_rating` and `average_rating` fields are calculated and saved
        """
        if trips.exists():
            rating_items = [
                trip.driver_rating for trip in trips if trip.driver_rating is not None]
            if len(rating_items):
                self.count_rating = len(rating_items)
                self.average_rating = sum(rating_items) / len(rating_items)
                self.save()

    def get_rating_levels(self, trips):
        """
        Get passenger's ratings by levels (1-star, 2-star... etc.).

        Returns
        -------
        dict object with counts for each star rating (1-5).
        """
        rating_counts = {f'star_{i}': 0 for i in range(1, 6)}
        for trip in trips:
            rating = trip.driver_rating

            if f'star_{rating}' in rating_counts:
                rating_counts[f'star_{rating}'] += 1

        return rating_counts


class DriverProfile(models.Model):
    """
    Driver role-specific profile.
    Related to `Profile` model by one-to-one relationship.

    Stores driver status, experience and ratings received from user's completed trips.
    """

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='driver_profile')
    experience = models.IntegerField(default=2)
    average_rating = models.FloatField(default=0.0)
    count_rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Driver: {self.profile.user.username}"
    
    @property
    @admin.display(ordering="profile")
    def status(self):
        return self.profile.status
    
    def update_rating(self, trips):
        """
        Update driver's rating statistics.

        `count_rating` and `average_rating` fields are calculated and saved
        """
        if trips.exists():
            rating_items = [
                trip.passenger_rating for trip in trips if trip.passenger_rating is not None]
            if len(rating_items):
                self.count_rating = len(rating_items)
                self.average_rating = sum(rating_items) / len(rating_items)
                self.save()

    def get_rating_levels(self, trips):
        """
        Get driver's ratings by levels (1-star, 2-star... etc.).

        Returns
        -------
        dict object with counts for each star rating (1-5).
        """
        rating_counts = {f'star_{i}': 0 for i in range(1, 6)}
        for trip in trips:
            rating = trip.passenger_rating

            if f'star_{rating}' in rating_counts:
                rating_counts[f'star_{rating}'] += 1

        return rating_counts


class ManagerProfile(models.Model):
    """
    Manager role-specific profile.
    Related to `Profile` model by one-to-one relationship.

    Stores experience and ratings received from passenger and drivers's completed and rated trips.
    """
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='manager_profile')

    experience = models.IntegerField(null=True, blank=True)
    passenger_count_rating = models.IntegerField(null=True, blank=True)
    passenger_average_rating = models.DecimalField(
        null=True, blank=True, max_digits=2, decimal_places=1)
    driver_count_rating = models.IntegerField(null=True, blank=True)
    driver_average_rating = models.DecimalField(
        null=True, blank=True, max_digits=2, decimal_places=1)


    def __str__(self):
        return f"Manager: {self.profile.user.username}"

    @property
    @admin.display(ordering="profile")
    def status(self):
        return self.profile.status
    
    def update_rating(self, trips):
        """
        Updates the passengers and drivers rating statistics.

        Driver and passenger's `*_count_rating` and `*_average_rating` fields are calculated and saved
        """
        if trips.exists():
            passenger_rating_items = [
                trip.passenger_rating for trip in trips if trip.passenger_rating is not None]
            self.passenger_count_rating = len(passenger_rating_items)
            self.passenger_average_rating = sum(
                passenger_rating_items) / len(passenger_rating_items)

            driver_rating_items = [
                trip.driver_rating for trip in trips if trip.driver_rating is not None]
            self.driver_count_rating = len(driver_rating_items)
            self.driver_average_rating = sum(
                driver_rating_items) / len(driver_rating_items)

            self.save()

    def get_rating_levels(self, trips):
        """
        Get all passenger's ratings by levels from all completed and rated trip.
        only passenger rating is used to reflect overall performance of the service.

        Returns
        -------
        dict object with counts for each star rating (1-5).
        """
        if trips.exists():
            rating_counts = {f'star_{i}': 0 for i in range(1, 6)}
            for trip in trips:
                rating = trip.passenger_rating

                if f'star_{rating}' in rating_counts:
                    rating_counts[f'star_{rating}'] += 1

            return rating_counts
