from django.db import models

# Create your models here.
class dataModel(models.Model):
    title = models.CharField(max_length=100)
    views = models.IntegerField()
    duration = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    videoformat = models.CharField(max_length=50,default="mp4")
    resolution = models.CharField(max_length=50,default="720")
    content_type = models.CharField(max_length=50)



class CheckModel(models.Model):
    videoformat = models.BooleanField(default=True)
    resolution = models.BooleanField(default=True)
    content_type = models.BooleanField(default=True)
