from django.db import models

# Create your models here.
class dataModel(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    views = models.IntegerField()
    duration = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    content_type = models.CharField(max_length=50)
    OPTIONS1=[('1',"mp4"),('2',"WebM"),('3',"3GP")]
    OPTIONS2=[('1',"720p"),('2',"480p"),('3',"360p")]
    videoformat = models.CharField(max_length=20, choices=OPTIONS1)
    resolution = models.CharField(max_length=20, choices=OPTIONS2)




