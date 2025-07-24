from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

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
]


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='passenger')

    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
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
        except:
            avatar = static('images/avatar.png')
        return avatar


class PassengerProfile(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='passenger_profile')
    emergency_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Passenger: {self.profile.user.username}"


class DriverProfile(models.Model):

    DRIVER_STATUS_OPTIONS = [
        ('available', 'Available'),
        ('engaged', 'Engaged'),
        ('unavailable', 'Unavailable'),
    ]
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='driver_profile')
    experience = models.IntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=50, choices=DRIVER_STATUS_OPTIONS, default="available")

    def __str__(self):
        return f"Driver: {self.profile.user.username}"
    
    def update_status(self, status):
        self.status = status
        self.save()
