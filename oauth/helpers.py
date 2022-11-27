
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status
import requests
from helpers.helpers import check_response
from core.models import User


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
        # print()
    return ValidationError(detail="Error connecting to the Github Server", status=status.HTTP_400_BAD_REQUEST)


def get_github_user_profile(code):
    google_access_token_respone = requests.post(settings.GOOGLE_OAUTH_CONFIG['token_uri'], data={
        'client_id': settings.GOOGLE_OAUTH_CONFIG['client_id'],
        'client_secret': settings.GOOGLE_OAUTH_CONFIG['client_secret'],
        'code': code,
        'redirect_uri': settings.GOOGLE_OAUTH_CONFIG['redirect_uri'],

    }, headers={
        'Accept': 'application/json'
    })
    check_response(google_access_token_respone, "Get github access token")

    access_token_json = google_access_token_respone.json()

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
        # print()
    return ValidationError(detail="Error connecting to the Github Server", status=status.HTTP_400_BAD_REQUEST)


def check_oauth_user_exists(profile, oauth_id_field: str):
    user_filter = {
        oauth_id_field: profile['id'],
        'email': profile['email']
    }
    user = User.objects.filter(**user_filter)

    if user.exists():
        return user
    return None


def get_or_create_oauth_user(profile, oauth_id_field: str):
    if oauth_id_field is None:
        raise ValueError('oauth_id_field is required')

    user = check_oauth_user_exists(profile, oauth_id_field)
    if user is not None:
        return user.first()

    parsed_name = parse_fullname(profile['name'])

    user_data = {
        'email': profile['email'],
        'first_name': parsed_name['first_name'],
        'last_name': parsed_name['last_name'],
        oauth_id_field: profile['id'],
        'email_verified': True,
    }

    user = User.objects.create(
        **user_data
    )

    return user


def parse_fullname(fullname: str):
    splitted_name = fullname.split(' ')
    return {
        'first_name': splitted_name[0],
        'last_name': ' '.join(splitted_name[1:])
    }
