from django.db import models


class Dummy(models.Model):
    dummy_field = models.TextField()


class AbstractDummy(Dummy):
    class Meta:
        abstract = True
