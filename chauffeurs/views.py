from django.shortcuts import render

def chauffeurs_view(request):
    return render(request,'chauffeurs/chauffeurs.html')

