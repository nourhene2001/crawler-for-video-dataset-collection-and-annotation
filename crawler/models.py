from django.db import models
from rest_framework import serializers
# Create your models here.
class dataModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    views = models.IntegerField()
    duration = models.TimeField()
    url = models.CharField(max_length=255)
    videoformat = models.CharField(max_length=50,default="mp4")
    resolution = models.CharField(max_length=50,default="720")
    content_type = models.CharField(max_length=50)

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = dataModel
        fields = ["title","views","duration","description","url"]

class CheckModel(models.Model):
    videoformat = models.BooleanField(default=True)
    resolution = models.BooleanField(default=True)
    content_type = models.BooleanField(default=True)
