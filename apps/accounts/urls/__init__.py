from django.urls import path, include
from . import authentication, profile


app_name = 'accounts'
urlpatterns = [
    path("", include(authentication)),
    path("", include(profile)),
]
