from django.urls import path, include
from .views import  GoogleOAuthRedirectViewSet, get_github_user_profile,get_google_oauth_authorization_url,get_github_oauth_authorization_url,LoginUserView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register('oauth/google/redirect', GoogleOAuthRedirectViewSet,
                basename='google_oauth_redirect')

# router.register('user', LoginUserViewSet,basename="user-login")


urlpatterns = [
    path('oauth/google/authorization_url/',get_google_oauth_authorization_url,name='google_oauth_authorization_url'),
    path('oauth/github/authorization_url/',get_github_oauth_authorization_url,name='github_oauth_authorization_url'),
    path('oauth/github/redirect/', get_github_user_profile,
         name='github_oauth_redirect'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginUserView.as_view(), name='user-login'),
    path('', include(router.urls)),
]
