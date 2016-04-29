from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from series.models import Series


class Video(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='videos')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')

    series = models.ManyToManyField(Series, related_name='videos')
    ratings = models.ManyToManyField(User, through='Rating')

    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=255)

    def __str__(self):
        return "%s: %s" % (self.title, self.description)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    rating = models.IntegerField()

    def __str__(self):
        return str(self.rating)
