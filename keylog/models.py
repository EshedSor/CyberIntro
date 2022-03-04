from re import L
from django.db import models

# Create your models here.
class KeyLogStream(models.Model):
    source = models.CharField(max_length=50)
    stream = models.CharField(max_length=5000)
    created = models.DateTimeField(auto_created=True,auto_now_add=True)
    