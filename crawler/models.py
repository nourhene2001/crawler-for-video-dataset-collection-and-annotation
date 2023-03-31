from django.db import models

# Create your models here.

    #dataset_name=models.CharField(max_length=255)

class dataModel(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    views = models.IntegerField()
    duration = models.CharField(max_length=255)
    description = models.CharField(max_length=10000,null=True,blank=True)
    url = models.CharField(max_length=255)
    content_type = models.CharField(max_length=50,null=True,blank=True,default='')
    OPTIONS1=[('mp4',"mp4"),('WebM',"WebM"),('3GP',"3GP")]
    OPTIONS2=[('720p',"720p"),('480p',"480p"),('360p',"360p")]
    videoformat = models.CharField(max_length=20, choices=OPTIONS1,default="mp4")
    resolution = models.CharField(max_length=20, choices=OPTIONS2,default="720p")

    def __iter__(self):
        return iter(self.data)


class datasetModel(models.Model):
    id=models.AutoField(primary_key=True)
    name= models.CharField(max_length=255, unique=True, blank=True)
    creation_date=models.DateTimeField()
    num_video=models.IntegerField(default=0)
    min_v=models.CharField(max_length=255, blank=True)
    max_v=models.CharField(max_length=255,blank=True)
    description=models.CharField(max_length=1000,blank=True)
    videos = models.ManyToManyField(dataModel, through='video_dataset',through_fields=('dataset', 'videos'))


    def __iter__(self):
        return iter(self.data)

class video_dataset(models.Model):
    id=models.AutoField(primary_key=True)
    dataset = models.ForeignKey(datasetModel, on_delete=models.CASCADE)
    videos = models.ForeignKey(dataModel, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True) 





