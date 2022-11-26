from rest_framework import serializers
from django.conf import settings
from core.models import User
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from rest_framework import exceptions

class OauthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=255)
