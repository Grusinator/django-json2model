from django.db import models


class Dummy(models.Model):
    dummy_field = models.TextField()

    class Meta:
        abstract = True


class AbstractDummy(Dummy):
    class Meta:
        abstract = True
