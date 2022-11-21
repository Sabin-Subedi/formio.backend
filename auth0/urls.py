from django.urls import path
from .views import google_oauth_url

urlpatterns = [
    path('oauth/google',google_oauth_url)
]
