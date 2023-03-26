from django.contrib import admin

from crawler.models import  dataModel, datasetModel

# Register your models here.

admin.site.register(dataModel)
admin.site.register(datasetModel)