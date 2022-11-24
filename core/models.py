from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
from django.apps import apps
from helpers.models import BaseModel
from django.contrib.auth.validators import UnicodeUsernameValidator



class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(blank=False, unique=True)
    email_verified = models.BooleanField(default=False)
    google_oauth = models.JSONField(blank=True,null=True)
    github_oauth = models.JSONField(blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# class OAuth(models.Model):
    