"""
URL configuration for project project.

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
from random import random
from django.http import HttpResponse
from app_datetime.views import datetime_view
from project.settings import DEBUG


def random_view(request):
    if request.method == "GET":
        data = random()
        return HttpResponse(data)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('random/', random_view),
    path('datetime/', datetime_view),
    path('weather/', include('app_weather.urls')),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('login/', include('app_login.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
]

if DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]