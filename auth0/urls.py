from django.urls import path, include
from .views import GoogleOAuthViewSet, GoogleOAuthRedirectViewSet, GithubOAuthViewSet, get_github_user_profile
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('oauth/google/', GoogleOAuthViewSet,
                basename='google_oauth_url')
router.register('oauth/google/redirect/', GoogleOAuthRedirectViewSet,
                basename='google_oauth_redirect')
router.register('oauth/github/', GithubOAuthViewSet,
                basename='github_oauth_url')
# router.register('oauth/github/redirect/', GithubOAuthRedirectViewSet,
#                 basename='github_oauth_redirect')


urlpatterns = [
    path('oauth/github/redirect/', get_github_user_profile,
         name='github_oauth_redirect'),
    path('', include(router.urls)),
]
