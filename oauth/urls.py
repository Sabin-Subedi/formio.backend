from django.urls import path
from . import views
urlpatterns = [
    path('github/',views.github_oauth_authorization_url,name="github_oauth"),
    # path('github/redirect/',views.github_redirect_url,name="github_callback"),
]
