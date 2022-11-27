from rest_framework import serializers
from django.conf import settings
from core.models import User
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from rest_framework import exceptions


class UserSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField(
        method_name="get_tokens", read_only=True, required=False)

    class Meta:
        model = User
        fields = ['idx', 'email', 'password', 'first_name', 'last_name', 'last_login',
                  'created_at', 'is_active', 'email_verified', 'google_oauth_id', 'github_oauth_id', 'tokens']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def get_tokens(self, user):
        return self.context['token']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        self.user = authenticate(
            email=attrs['email'], password=attrs['password'])

        if self.user is None:
            raise exceptions.AuthenticationFailed()

        return {}


class OauthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=255)
