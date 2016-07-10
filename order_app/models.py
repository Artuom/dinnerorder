from __future__ import unicode_literals

from django.db import models

# Create your models here.


class DUserModel(models.Model):
    item = models.CharField(max_length=100)
    whom = models.CharField(max_length=100)
    e_mail = models.EmailField()
    byr = models.IntegerField(null=True)
    byn = models.FloatField(null=True)
    comment = models.CharField(max_length=200)

    def __unicode__(self):
        return self.item
