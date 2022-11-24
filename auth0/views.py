import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .helpers import oauth_google_authorization_url
from rest_framework.status import HTTP_400_BAD_REQUEST
from pprint import pprint
from django.conf import settings

# Create your views here.


class GoogleOAuthViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        return Response(oauth_google_authorization_url)


class GoogleOAuthRedirectViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        if request.query_params.get('error'):
            raise AuthenticationFailed(request.query_params.get('error'))

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/userinfo.email',
                    'https://www.googleapis.com/auth/userinfo.profile'],
            redirect_uri='http://localhost:8000/auth/oauth/google/redirect/'
        )

        flow.fetch_token(code=request.query_params.get('code'))
        credentials = credentials_to_dict(flow.credentials)

        profile_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                                        params={"alt": "json", "access_token": credentials["token"]})
        check_response(profile_response, "Get user profile")
        userInfo = profile_response.json()

        return Response(userInfo)


class GithubOAuthViewSet(GenericViewSet):
    http_method_names = ['get']

    def list(self, request):
        authorize_url = gen_url(
            url='https://github.com/login/oauth/authorize',
            params={'client_id': settings.GITHUB_OAUTH_CONFIG['client_id'],
                    'redirect_uri': settings.GITHUB_OAUTH_CONFIG['redirect_uri'],
                    'scope': settings.GITHUB_OAUTH_CONFIG['scope']
                    }
        )

        return Response(authorize_url)


@api_view(['GET'])
def get_github_user_profile(request):

    if request.query_params.get('error'):
        raise AuthenticationFailed(
            request.query_params.get('error_description'))

    github_access_token_respone = requests.post('https://github.com/login/oauth/access_token', data={
        'client_id': settings.GITHUB_OAUTH_CONFIG['client_id'],
        'client_secret': settings.GITHUB_OAUTH_CONFIG['client_secret'],
        'code': request.query_params.get('code'),
        'redirect_uri': settings.GITHUB_OAUTH_CONFIG['redirect_uri'],

    }, headers={
        'Accept': 'application/json'
    })
    check_response(github_access_token_respone, "Get github access token")

    access_token_json = github_access_token_respone.json()

    if access_token_json.get('error'):
        raise AuthenticationFailed(
            access_token_json.get('error_description'))

    # return Response(access_token_json)

    if access_token_json.get('access_token'):
        access_token = access_token_json.get('access_token')
        pprint(access_token)
        github_user_profile_response = requests.get('https://api.github.com/user', headers={
            'Authorization': 'Bearer ' + access_token
        })
        check_response(github_user_profile_response, "Get github user profile")
        github_user_profile = github_user_profile_response.json()
        github_user_profile['access_token'] = access_token

        print(github_user_profile['email'])

        if github_user_profile['email'] is None:

            github_user_email_response = requests.get('https://api.github.com/user/emails', headers={
                'Accept': 'application/vnd.github+json',
                'Authorization': 'Bearer ' + access_token,

            })
            check_response(github_user_email_response, "Get github user email")
            github_user_email_response = github_user_email_response.json()
            for item in github_user_email_response:
                if item['primary'] == True:
                    github_user_profile['email'] = item['email']

        return Response(github_user_profile)

        # print()
    return ValidationError(detail="Error connecting to the Github Server", status=HTTP_400_BAD_REQUEST)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def check_response(response, response_type):

    if response.status_code != 200:
        raise ValidationError(
            detail="There was some issue with oauth", code=response.status_code)


def gen_url(url, params):
    query_strings = []
    for key, value in params.items():

        query_strings.append('{}={}'.format(
            key, ",".join(value) if type(value) == list else value))
    return url + '?' + '&'.join(query_strings)
