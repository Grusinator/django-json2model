# Create your models here.
from django.db import models
from jsonfield import JSONField

from json2model.services.dynamic_model import create_objects_from_json


class CreateRequest(models.Model):
    root_name = models.TextField()
    json_data = JSONField()
    status = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        create_objects_from_json(self.root_name, self.json_data)