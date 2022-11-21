from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class User(settings.APP_BASE_MODEL,AbstractUser):
    email = models.EmailField(required=True,blank=False)
    emailVerified = models.BooleanField(default=False)
    registeredAt = models.DateTimeField(auto_now_add=True)

