from django.contrib import admin

from crawler.models import  dataModel, datasetModel, video_dataset

# Register your models here.

admin.site.register(dataModel)
admin.site.register(datasetModel)
admin.site.register(video_dataset)