from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import DriverProfile

def chauffeurs_view(request):
    chauffeurs = DriverProfile.objects.all()
    context = {
        'chauffeurs': chauffeurs,
        'user': request.user,
        'mystring': 'Hello World',
    }
    return render(request, 'chauffeurs/chauffeurs.html', context)
