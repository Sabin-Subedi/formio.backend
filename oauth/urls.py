from django.urls import path
from . import views
urlpatterns = [
    path('google/', views.google_oauth_authorization_url, name="github_oauth"),
    path('github/', views.github_oauth_authorization_url, name="github_oauth"),
    path('github/login/', views.oauth_github, name="github_callback"),
]
