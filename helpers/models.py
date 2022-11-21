from django.db import models
from uuid import uuid4

# Create your models here.
class BaseModel(models.Model):
    idx = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)