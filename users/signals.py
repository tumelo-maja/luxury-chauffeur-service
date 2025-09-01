"""
User app signals.

Defines Django signal handlers for the `User` model.
It ensures that profiles and email addresses are automatically
created or updated when a User object is saved.

user_presave - Triggered before a User is saved.
    Ensures the username is always stored in lowercase.
user_postsave - Triggered after a User is saved.
    Creates a Profile for new users,
    and updates the EmailAddress model for existing users.
"""
from allauth.account.models import EmailAddress
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from .models import Profile


@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    """
    Handles pre-save actions for User.
    Ensures that all usernames are stored in lowercase before saving.

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (User).
    instance : User
        The actual user instance being saved.
    **kwargs : dict
        Additional keyword arguments passed by the signal.
    """
    if instance.username:
        instance.username = instance.username.lower()


@receiver(post_save, sender=User)
def user_postsave(sender, instance, created, **kwargs):
    """
    Handles post-save actions for User.
    Creates a Profile object when a new User is created.
    Also used for updating the user's email address

    Parameters
    ----------
    sender : Model
        The model class that sent the signal (User).
    instance : User
        The actual user instance being saved.
    created : bool
        True if a new record was created, False if updated.
    **kwargs : dict
        Additional keyword arguments passed by the signal.
    """

    user = instance
    if created:
        Profile.objects.create(user=user)
    else:
        try:
            email_address = EmailAddress.objects.get_primary(user)
            if email_address:
                if email_address.email != user.email:
                    email_address.email = user.email
                    email_address.verified = False
                    email_address.save()
        except EmailAddress.DoesNotExist:
            EmailAddress.objects.create(
                user=user,
                email=user.email,
                primary=True,
                verified=False
            )
