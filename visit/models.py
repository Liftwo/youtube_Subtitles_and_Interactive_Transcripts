from django.db import models
from django.contrib import admin


class Visit(models.Model):
    times = models.IntegerField()

    def __str__(self):
        return self.times


class Like(models.Model):
    like_times = models.IntegerField()


class Collect(models.Model):
    video_id = models.CharField(max_length=11)
    json_dual = models.TextField(blank=True, null=False, default='n')
    rate = models.IntegerField(default=1)
    video_title = models.TextField(blank=True, null=False, default='n')

    def __str__(self):
        return self.video_title

