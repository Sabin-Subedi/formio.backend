import requests
from django.conf import settings
from helpers.helpers import check_response
from .helpers import credentials_to_dict
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
from core.models import User
import google_auth_oauthlib


def get_github_user_profile(code):
    github_access_token_respone = requests.post('https://github.com/login/oauth/access_token', data={
        'client_id': settings.GITHUB_OAUTH_CONFIG['client_id'],
        'client_secret': settings.GITHUB_OAUTH_CONFIG['client_secret'],
        'code': code,
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

        return github_user_profile

    return ValidationError(detail="Error connecting to the Github Server", status=status.HTTP_400_BAD_REQUEST)


def check_oauth_user_exists(profile, oauth_id_field: str):
    user = User.objects.filter(email=profile['email'])
    if user.exists() and profile['id'] == user.first()[oauth_id_field]:
        return user
    return None


def get_or_create_user(profile, oauth_id_field: str):
    user = check_oauth_user_exists(profile, oauth_id_field)
    if user is not None:
        return user.first()

    user = User.objects.create(
        email=profile['email'],
        first_name=profile['name'],
        oauth_id=profile['id'],
        oauth_id_field=oauth_id_field,
        oauth_access_token=profile['access_token']
    )

    return user


def get_google_user_profile(code):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_OAUTH_CONFIG['client_secret_file'],
        scopes=settings.GOOGLE_OAUTH_CONFIG['scope'],
        redirect_uri=settings.GOOGLE_OAUTH_CONFIG['redirect_uri'])

    flow.fetch_token(code=code)
    credentials = credentials_to_dict(flow.credentials)

    profile_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                                    params={"alt": "json", "access_token": credentials["token"]})
    check_response(profile_response, "Get user profile")
    userInfo = profile_response.json()
    return userInfo
