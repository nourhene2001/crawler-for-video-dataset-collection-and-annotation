import json
from zipfile import ZipFile
from celery import shared_task
from django import apps
from django.core import serializers

import pytube
import os

from crawler.models import datasetModel

@shared_task
def download_videos(pk):
    print('MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMk')
    instance=datasetModel.objects.get(pk=pk)
    print('MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')
    videos = instance.videos.all()
    downloaded_videos = []
    for video in videos:
        yt = pytube.YouTube(video.url)
        stream = yt.streams.filter(res=instance.resolution, file_extension=instance.videoformat).first()
        if stream is not None:
            video_path = stream.download(output_path=instance.folder)
            print(video_path)
            downloaded_videos.append(video_path)
        else:
            stream = yt.streams.filter(res=instance.resolution, file_extension="mp4").first()
            video_path = stream.download(output_path=instance.folder)
            print(video_path)
            downloaded_videos.append(video_path)

