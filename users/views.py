from allauth.account.utils import send_email_confirmation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login
from django.urls import reverse
from django.db import transaction
from .forms import *
from .models import *

# Create your views here.


@login_required
def profile_view(request, username):
    if username != request.user:
        profile = get_object_or_404(User, username=username).profile
    else:
        profile = request.user.profile
                
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_edit_view(request):

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

    role_form = form(instance=role)
    if request.path == reverse('profile-onboarding'):
        is_new_user = True
    else:
        is_new_user = False

    context ={
        'profile_form': profile_form,
        'role_form': role_form,
        'is_new_user': is_new_user,
        'user_type': profile_user.user_type
    }
    return render(request, 'users/profile-edit.html', context)

@login_required
def profile_settings_view(request):
    return render(request, 'users/profile-settings.html')

@login_required
def profile_settings_partial_view(request):

    if request.htmx:
        form = ProfileSettingsForm(instance=request.user)
        return render(request, 'partials/settings-form.html', {'form':form})

    if request.method == "POST":
        form = ProfileSettingsForm(request.POST, instance=request.user)

        if form.is_valid():

            # Check if the email already exists 
            email= form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f"{email} is already in use.")
                return redirect('profile-settings')
            
            form.save()
            messages.success(request, "Success! Changes saved.")
            # Then signal.py updates emailaddresses and set verified to False

            #send verification email
            send_email_confirmation(request, request.user)

            return redirect('profile-settings')
        
        else:
            messages.warning(request, "Form not valid")
            return redirect('profile-settings')
                
    
    return redirect('home')

@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')

@login_required
def profile_delete_view(request):
    user =request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted! See you next time')
        return redirect('home')
        
    return render(request, 'users/profile-delete.html')

def signup_type(request):

    return render(request, 'account/signup-type.html')

def driver_signup(request):

    if request.method == 'POST':
        form = MainSignupForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.user_type = 'driver'
                user.save()

            messages.success(request, "Driver's account created successfully.")
            send_email_confirmation(request, user)

            return redirect('account-success')
    else:
        form = MainSignupForm()

    context = {
        'form': form,
        'user_type': 'driver',
    }
    return render(request, 'account/signup-form.html',context )

def passenger_signup(request):

    if request.method == 'POST':
        form = MainSignupForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(commit=False)
            user.user_type = 'passenger'
            user.save()

            messages.success(request, "Passenger's account created successfully.")
            send_email_confirmation(request, user)

            return redirect('account-success')
    else:
        form = MainSignupForm()
    
    context = {
        'form': form,
        'user_type': 'passenger',
    }
    return render(request, 'account/signup-form.html', context)


def account_success(request):
    return render(request, 'users/account-created.html')
