"""
URL configuration for chauffeur services project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import home_view
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',  include('allauth.urls')),
    path('accounts/signup/', include('users.urls')),
    path('profile/', include('users.urls')),
    path('chauffeurs/', include('chauffeurs.urls')),
    path('trips/', include('trips.urls')),
    path('', home_view, name="home"),
]

# to Be removed fir production
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
