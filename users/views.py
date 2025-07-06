from allauth.account.utils import send_email_confirmation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login
from django.urls import reverse
from django.db import transaction
from .forms import *

# Create your views here.


@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_edit_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if profile.user_type == 'driver':
        driver_profile, created = DriverProfile.objects.get_or_create(profile=profile)
        form = DriverEditForm
        role = driver_profile
    else:
        passenger_profile, created = PassengerProfile.objects.get_or_create(profile=profile)
        form = PassengerEditForm
        role = passenger_profile

    if request.method == 'POST':
        profile_form = ProfileEditForm(
            request.POST, 
            request.FILES, 
            instance=profile
        )
        role_form = form(
            request.POST, 
            instance=role
        )
        
        if profile_form.is_valid() and role_form.is_valid():
            profile_form.save()
            role_form.save()
            
            return redirect('home')
    else:
        profile_form = ProfileEditForm(instance=profile)
        role_form = form(instance=role)
    
    if request.path == reverse('profile-onboarding'):
        is_new_user = True
    else:
        is_new_user = False  
    
    context ={
        'profile_form': profile_form,
        'role_form': role_form,
        'is_new_user': is_new_user,
        'user_type': 'driver' if profile.user_type == 'driver' else 'passenger'
    }
    return render(request, 'users/profile_edit.html', context)

@login_required
def profile_settings_view(request):

    return render(request, 'users/profile_settings.html')

@login_required
def profile_settings_partial_view(request):

    if request.htmx:
        form = ProfileSettingsForm(instance=request.user)
        return render(request, 'partials/settings_form.html', {'form':form})

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
        
    return render(request, 'users/profile_delete.html')

def signup_type(request):

    return render(request, 'account/signup_type.html')

def driver_signup(request):

    if request.method == 'POST':
        form = MainSignupForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.user_type = 'driver'
                user.save()

            messages.success(request, "Driver's account created successfully.")
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile-onboarding')
    else:
        form = MainSignupForm()

    context = {
        'form': form,
        'user_type': 'driver',
    }
    return render(request, 'account/signup_form.html',context )

def passenger_signup(request):

    if request.method == 'POST':
        form = MainSignupForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.user_type = 'passenger'
                user.save()

            messages.success(request, "Passenger's account created successfully.")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile-onboarding')
    else:
        form = MainSignupForm()
    
    context = {
        'form': form,
        'user_type': 'passenger',
    }
    return render(request, 'account/signup_form.html', context)

