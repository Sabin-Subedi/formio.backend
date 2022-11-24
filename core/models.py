from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
from django.apps import apps
from helpers.models import BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(blank=False, unique=True)
    emailVerified = models.BooleanField(default=False)
    registeredAt = models.DateTimeField(auto_now_add=True)
    googleOauth = models.JSONField(blank=True)
