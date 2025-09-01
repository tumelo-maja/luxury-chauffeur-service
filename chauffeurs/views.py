from django.shortcuts import render
from users.models import DriverProfile


def chauffeurs_view(request):
    """
    Display a grid list of all registered chauffeurs.

    Returns
    -------
    Rendered template displaying the list
        of chauffeurs each with their DriverProfile details.
    """
    chauffeurs = DriverProfile.objects.all()
    context = {
        'chauffeurs': chauffeurs,
        'user': request.user,
    }
    return render(request, 'chauffeurs/chauffeurs.html', context)
