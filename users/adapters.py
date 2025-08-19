"""
Custom adapters for the `users` app.

Handles social account adapters for social logins
and role-specific profile creations
"""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.shortcuts import resolve_url
from .models import PassengerProfile, DriverProfile


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for general account flow.
    """    
    def get_signup_redirect_url(self, request):
        """
        Defines the redirect URL path after successful signup.

        Returns
        -------
        str
            URL for the `profile-onboarding` view.
        """        
        return resolve_url("profile-onboarding")


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Social Custom adapter for handling social account authentication.
    """

    def pre_social_login(self, request, sociallogin):
        """
        Triggered before completing a social login.

        Updates/creates the email address from the social provider and marked it as verified.
        user with existing email address is linked to the social login 
        """

        email = sociallogin.account.extra_data.get("email")
        if not email:
            return

        if sociallogin.is_existing:
            user = sociallogin.user
            email_address, created = EmailAddress.objects.get_or_create(
                user=user, email=email)
            if not email_address.verified:
                email_address.verified = True
                email_address.save()

    def save_user(self, request, sociallogin, form=None):
        """
        Save a new user authenticated via social login.

        Associates an email address, verifies it,
        and creates a role-specific profile if one does not exist.
        Uses the `role` query parameter stored in the session to determine user's role
        """   

        user = super().save_user(request, sociallogin, form)
        email = user.email
        email_address, created = EmailAddress.objects.get_or_create(
            user=user, email=email)
        if not email_address.verified:
            email_address.verified = True
            email_address.save()

        role = request.session.get('role')
        profile = user.profile
        profile.user_type = role
        profile.save()        
        if role == 'driver':
            DriverProfile.objects.get_or_create( profile=profile)
        elif role == 'passenger':
            PassengerProfile.objects.get_or_create( profile=profile)

        # Remove `role` from request.session
        request.session.pop('role', None)

        return user
