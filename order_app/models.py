from __future__ import unicode_literals

from django.db import models

# Create your models here.


class DUserModel(models.Model):
    item = models.CharField(max_length=100)
    whom = models.CharField(max_length=100, blank=True)
    e_mail = models.EmailField(blank=True)
    byr = models.IntegerField(blank=True, null=True)
    byn = models.FloatField(null=True, blank=True)
    comment = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.item
