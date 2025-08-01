from allauth.account.models import EmailAddress
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import Profile, DriverProfile, PassengerProfile


@receiver(post_save, sender=User)
def user_postsave(sender, instance, created, **kwargs):
    user = instance

    # add profile when user is created
    if created:

        profile = Profile.objects.create(user=user)
            
        if user.user_type == 'driver':
            profile.user_type = 'driver'
            profile.save()
            DriverProfile.objects.create(profile=profile)
        elif user.user_type ==  'passenger':
            profile.user_type = 'passenger'
            profile.save()
            PassengerProfile.objects.create(profile=profile)
            
    else:
        #update allauth emailaddresse if exist else create one
        try:
            email_address = EmailAddress.objects.get_primary(user)

            if email_address.email !=user.email:
                email_address.email= user.email
                email_address.verified= False
                email_address.save()
            
        except :
            EmailAddress.objects.create(
                user = user,
                email =user.email,
                primary = True,
                verified = False
            )        

@receiver(pre_save,sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()
