from django.shortcuts import render,redirect
from .helpers import oauth_google_authorization_url
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery
from google.oauth2 import id_token
from google.auth.transport import requests

from core.models import User
import requests
# Create your views here.

hello = None

class GoogleOAuthViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        return Response(oauth_google_authorization_url)


class GoogleOAuthRedirectViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        print(request)
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri = 'http://localhost:8000/auth/oauth/google/redirect/'
        )

        flow.fetch_token(code=request.query_params.get('code'))
        credentials = credentials_to_dict(flow.credentials)
        
        profileResponse = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                                          params={"alt": "json", "access_token": credentials["token"]})
        check_response(profileResponse, "Get user profile")
        userInfo = profileResponse.json()
        

        
        return Response(userInfo)

class GoogleOAuthDoneViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        if hello is  None:
            return redirect(to='/auth/oauth/google/')
    
        newCredentials = google.oauth2.credentials.Credentials(
                **hello
            )
      
        return Response("ok")
    
@api_view()
def auth_route(request):
    pass
    

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


@api_view()
def google_oauth_redirect(req):
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    return Response('google_oauth_redirect')

def check_response(response: requests.Response, requestType: str):
    if response.status_code != 200:
        auth_logger.error(
            f"{requestType} request was not successful. "
            "Cause: request to Google OAuth Server Failed, "
            f"with status code {response.status_code} and reason {response.reason}"
        )
        raise Exception("Error encountered while connecting to Google Oauth Server.")