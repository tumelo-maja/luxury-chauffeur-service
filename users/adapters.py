from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.shortcuts import resolve_url
from .models import PassengerProfile, DriverProfile


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        return resolve_url("profile-onboarding")


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email")

        role = request.GET.get('role')
        print("Weeeeeeeeeeee found it - SocialAccountAdapter")

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
        user = super().save_user(request, sociallogin, form)
        email = user.email
        email_address, created = EmailAddress.objects.get_or_create(
            user=user, email=email)
        if not email_address.verified:
            email_address.verified = True
            email_address.save()

        # role = request.GET.get('role')
        print("Weeeeeeeeeeee found it - save_user")
        print(request)
        # Profile.objects.create(user=user)
        print("profile below")
        print(user.profile)
        role = request.session.get('role')
        profile = user.profile
        profile.user_type = role
        profile.save()        
        if role == 'driver':
            DriverProfile.objects.get_or_create( profile=profile)
        elif role == 'passenger':
            PassengerProfile.objects.get_or_create( profile=profile)

        request.session.pop('role', None)  #clear session

        return user
