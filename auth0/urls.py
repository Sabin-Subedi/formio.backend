from django.urls import path
from .views import GoogleOAuthViewSet, GoogleOAuthRedirectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('oauth/google/', GoogleOAuthViewSet,
                basename='google_oauth_url')
router.register('oauth/google/redirect/', GoogleOAuthRedirectViewSet,
                basename='google_oauth_url')


urlpatterns = router.urls
