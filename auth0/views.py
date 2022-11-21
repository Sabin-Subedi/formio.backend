from django.shortcuts import render
from .helpers import oauth_google_authorization_url
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view()
def google_oauth_url(req):
    url = {
        oauth_url : oauth_google_authorization_url
    }
    return Response(url)