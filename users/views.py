from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
                #need code to warn user
                return redirect('profile-settings')
            
            form.save()

            # Then signal.py updates emailaddresses and set verified to False

            return redirect('profile-settings')
                
    
    return redirect('home')