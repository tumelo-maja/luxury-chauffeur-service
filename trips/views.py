from django.shortcuts import render

# Create your views here.
def trip_view(request):
    return render(request,'trips/trip.html')