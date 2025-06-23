from django.db import models
from django.contrib.auth.models import User

TITLE_OPTIONS = [
                ('Mr', 'Mr'),
                ('Mrs', 'Mrs'),
                ('Ms', 'Ms'),
                ('Dr', 'Dr'),
                ('Prof', 'Prof'),
                ('Lord', 'Lord'),
                ('Sir', 'Sir'),
            ]

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    preferred_name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=20, choices=TITLE_OPTIONS, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    home_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Passenger: {self.user.username}"