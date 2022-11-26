import google_auth_oauthlib.flow
import requests
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from pprint import pprint
from .helpers import (credentials_to_dict, gen_auth_tokens)
from helpers.helpers import gen_url, check_response
from rest_framework.views import APIView
from .serializers import LoginSerializer, UserSerializer, OauthSerializer
from core.models import User
import json
from rest_framework.mixins import ListModelMixin

from rest_framework_simplejwt.views import token_obtain_pair
from django.contrib.auth import login

from . import oauth_helpers


@api_view(['GET'])
def get_google_oauth_authorization_url(request):
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_OAUTH_CONFIG['client_secret_file'],
        scopes=settings.GOOGLE_OAUTH_CONFIG['scope'],
        redirect_uri=settings.GOOGLE_OAUTH_CONFIG['redirect_uri'])

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    return Response({
        'authorization_url': authorization_url,
    })


@api_view(['GET'])
def get_github_oauth_authorization_url(request):
    authorize_url = gen_url(
        url='https://github.com/login/oauth/authorize',
        params={'client_id': settings.GITHUB_OAUTH_CONFIG['client_id'],
                'redirect_uri': settings.GITHUB_OAUTH_CONFIG['redirect_uri'],
                'scope': settings.GITHUB_OAUTH_CONFIG['scope']
                }
    )
    return Response({
        "authorization_url": authorize_url
    })


class GoogleOAuthRedirectViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        if request.query_params.get('error'):
            raise AuthenticationFailed(request.query_params.get('error'))

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH_CONFIG['client_secret_file'],
            scopes=settings.GOOGLE_OAUTH_CONFIG['scope'],
            redirect_uri=settings.GOOGLE_OAUTH_CONFIG['redirect_uri'])
        try: 
            flow.fetch_token(code=request.query_params.get('code'))
            credentials = credentials_to_dict(flow.credentials)

            profile_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                                            params={"alt": "json", "access_token": credentials["token"]})
            check_response(profile_response, "Get user profile")
            userInfo = profile_response.json()

            return Response(userInfo)
        except:
            flow.get




class GoogleOauthView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = OauthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = oauth_helpers.get_google_user_profile(
            serializer.validated_data['code'])

        user = oauth_helpers.get_or_create_user(user_profile)


class LoginUserView(APIView):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.user)
        login(self.request, user=serializer.user)
        user = User.objects.get(email=serializer.user)

        if user is None:
            raise ValidationError(
                "Your login info is not right. Try again, or reset your password. if it slipped your mind.", status=status.HTTP_401_UNAUTHORIZED)

        print(user)
        token = gen_auth_tokens(user)

        context = {"token": token}
        serialized_user = UserSerializer(user, context=context)

        return Response(serialized_user.data)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
