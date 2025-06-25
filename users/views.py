from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
