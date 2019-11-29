# Create your models here.
from django.db import models
from jsonfield import JSONField

class CreateRequest(models.Model):
    root_name = models.TextField()
    json_data = JSONField()
    status = models.IntegerField(default=0)