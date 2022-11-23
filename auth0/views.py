from django.shortcuts import render
from .helpers import oauth_google_authorization_url
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet
import google_auth_oauthlib.flow

# Create your views here.


class GoogleOAuthViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        return Response(oauth_google_authorization_url)


class GoogleOAuthRedirectViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'])

        flow.redirect_uri = 'http://localhost:8000/auth/oauth/google/redirect/'

        flow.fetch_token(code=request.query_params.get('code'))
        credentials = flow.credentials
        return Response(credentials_to_dict(credentials))

# @api_view()
# def google_oauth_url(req):

#     return Response(authorization_url)


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
