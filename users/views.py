from allauth.account.utils import send_email_confirmation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from .forms import *

# Create your views here.


def profile_view(request):
    profile = request.user.profile
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Success! Changes saved.")
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        is_new_user = True
    else:
        is_new_user = False    

    return render(request, 'users/profile_edit.html', {'form': form,'is_new_user':is_new_user})

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