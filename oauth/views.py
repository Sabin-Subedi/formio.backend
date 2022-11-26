from django.shortcuts import redirect
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response


from helpers.helpers import gen_url,gen_auth_tokens
from auth0.serializers import UserSerializer
from . import helpers
from . import serializers



@api_view(['GET'])
def github_oauth_authorization_url(request):
    authorize_url = gen_url(
        url='https://github.com/login/oauth/authorize',
        params={'client_id': settings.GITHUB_OAUTH_CONFIG['client_id'],
                'redirect_uri': settings.GITHUB_OAUTH_CONFIG['redirect_uri'],
                'scope': settings.GITHUB_OAUTH_CONFIG['scope']
                }
    )
    return redirect(authorize_url)

@api_view(['POST'])
def oauth_github(request):
    serializer = serializers.OauthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_profile = helpers.get_github_user_profile(
    serializer.validated_data['code'])

    user = helpers.get_or_create_user(user_profile,'github_oauth_id')
    
    token = gen_auth_tokens(user)
    context = {"token": token}
    serialized_user = UserSerializer(user, context=context)

    return Response(serialized_user.data)


@api_view(['GET'])
def google_oauth_authorization_url(request):
    authorize_url = gen_url(
        url=settings.GOOGLE_OAUTH_CONFIG['auth_uri'],
        params={'client_id': settings.GOOGLE_OAUTH_CONFIG['client_id'],
                'redirect_uri': settings.GOOGLE_OAUTH_CONFIG['redirect_uri'],
                'scope': settings.GOOGLE_OAUTH_CONFIG['scope']
                }
    )
    return redirect(authorize_url)
