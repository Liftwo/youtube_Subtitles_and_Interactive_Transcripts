from django.db import models
from django.contrib import admin


class Visit(models.Model):
    times = models.IntegerField()


class Like(models.Model):
    like_times = models.IntegerField()