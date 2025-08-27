"""
User app views.

This module contains views related to user profiles, settings, signup, and
account management.

"""
from allauth.account.utils import send_email_confirmation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from django.http import Http404
from .forms import *
from .models import *


@login_required
def profile_view(request, username):
    """
    Display a user's profile page. Accessible to logged-in users only

    Parameters
    ----------
    request : HttpRequest
        The current HTTP request object.
    username : str
        The username of the profile to view.

    Returns
    -------
    Rendered profile page for the user specified by `username`.
    """
    if username == request.user or request.user.profile.user_type == "manager":
        profile = get_object_or_404(User, username=username).profile
    else:
        raise Http404()        

    user_status = profile.status
    context = {
        'profile': profile,
        'user_status': user_status,
    }

    return render(request, 'users/profile.html', context)


@login_required
def profile_edit_view(request):
    """
    Display a user's profile page with editable fields. Logged-in users can only edit their own profiles.

    Rendered fields are user-role specific ie. according the associated user_type Profile

    Returns
    -------
    Rendered profile edit page for the logged-in user.
    Form validation and feedback are displayed as needed.
    User shown confirmation if profile update was successful. 
    """
    profile_user = request.user.profile
    profile_form = ProfileEditForm(instance=profile_user)

    if profile_user.user_type == 'driver':
        role = DriverProfile.objects.filter(profile=profile_user).first()
        form = DriverEditForm
    elif profile_user.user_type == 'passenger':
        role = PassengerProfile.objects.filter(profile=profile_user).first()
        form = PassengerEditForm
    else:
        role = ManagerProfile.objects.filter(profile=profile_user).first()
        form = ManagerEditForm

    if request.path == reverse('profile-onboarding'):
        is_new_user = True
    else:
        is_new_user = False

    if request.method == 'POST':
        profile_form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=profile_user
        )
        role_form = form(
            request.POST,
            instance=role
        )

        if profile_form.is_valid() and role_form.is_valid():
            profile_form.save()
            role_form.save()
            return redirect('profile', username=request.user)
        else:
            context = {
                'profile_form': profile_form,
                'role_form': role_form,
                'is_new_user': is_new_user,
                'user_type': profile_user.user_type
            }

            return render(request, 'users/profile-edit.html', context)

    role_form = form(instance=role)

    context = {
        'profile_form': profile_form,
        'role_form': role_form,
        'is_new_user': is_new_user,
        'user_type': profile_user.user_type
    }
    return render(request, 'users/profile-edit.html', context)


@login_required
def profile_settings_view(request):
    """
    Displays the profile settings page containing logged-in user's email address.

    Returns
    -------
    Rendered profile settings page for the logged-in user.
    """
    return render(request, 'users/profile-settings.html')


@login_required
def profile_settings_partial_view(request):
    """
    Swaps the email address display element with an editable, pre-filled email field from a partial template.

    Returns
    -------
    Rendered partial form if an HTMX request is used.
    Changes are saved if email address does not already exist for another user.

    """
    if request.htmx:
        form = ProfileSettingsForm(instance=request.user)
        return render(request, 'users/partials/settings-form.html', {'form': form})

    if request.method == "POST":
        form = ProfileSettingsForm(request.POST, instance=request.user)

        if form.is_valid():

            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f"{email} is already in use.")
                return redirect('profile-settings')

            form.save()
            messages.success(request, "Success! Changes saved.")

            # send verification email
            send_email_confirmation(request, request.user)

            return redirect('profile-settings')

        else:
            messages.warning(request, "Form not valid")
            return redirect('profile-settings')

    return redirect('home')


@login_required
def profile_emailverify(request):
    """
    Manually trigger sending of an email verification message for the logged-in user.

    Returns
    -------
    Redirects user to the profile settings page.
    """
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    """
    Displays a 'delete account' confirmation for the logged-in user and warns users about the next steps.

    If confirmed, user is logged-out and the account is removed from the database.

    Returns
    -------
    Rendered profile delete confirmation page.
    Logs user out and redirects to home page after account deletion.
    """
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted! See you next time')
        return redirect('home')

    return render(request, 'users/profile-delete.html')


def signup_type(request):
    """
    Displays the user-role selection signup page.

    Allows user to signup as a Chauffeur or as Passenger

    Returns
    -------
    Rendered signup type page.
    """
    return render(request, 'account/signup-type.html')


def user_signup(request):
    """
    Handles role Profile creation based on selected sign up role.

    Creates a new user and associates them with the chosen role
    (driver or passenger) profile.
    Sends email confirmation for verification after signup.

    Returns
    -------
    Rendered signup form page.
    Redirects user to account success page on valid signup.
    """
    role = request.session.get('role')

    if request.method == 'POST':
        form = MainSignupForm(data=request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.save()

            profile = user.profile
            profile.user_type = role
            profile.save()

            if role == 'driver':
                DriverProfile.objects.create(profile=profile)
            else:
                PassengerProfile.objects.create(profile=profile)

            messages.success(
                request, f"{role.capitalize()}'s account created successfully.")
            send_email_confirmation(request, user)

            # return redirect('account-success')
            return render(request, 'users/account-created.html',{'user_email': user.email })
        
        else:
            context = {
                'form': form,
                'user_type': role,
            }            
            return render(request, 'account/signup-form.html', context)

    else:

        form = MainSignupForm()
        form.fields['role'].initial = role

    context = {
        'form': form,
        'user_type': role,
    }
    return render(request, 'account/signup-form.html', context)


def account_success(request):
    """
    Displays the account creation success page.
    Message to confirm account is shown to user

    Returns
    -------
    Rendered account success page.
    """
    return render(request, 'users/account-created.html')
