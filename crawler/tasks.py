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
    f=instance.folder+"\\videos"
    downloaded_videos = []
    for video in videos:
        yt = pytube.YouTube(video.url)
        stream = yt.streams.filter(res=instance.resolution, file_extension=instance.videoformat).first()
        if stream is not None:
            video_path = stream.download(output_path=f)
            
            print(video_path)
            i=0
            # Rename the downloaded video file to i+1
            new_video_path = os.path.join(f, f"{i+1}.{instance.videoformat}")
            os.rename(video_path, new_video_path)
            downloaded_videos.append(new_video_path)
        else:
            stream = yt.streams.filter(res=instance.resolution, file_extension="mp4").first()
            video_path = stream.download(output_path=f)
            print(video_path)
            i=0
                            # Rename the downloaded video file to i+1
            new_video_path = os.path.join(f, f"{i+1}.mp4")
            os.rename(video_path, new_video_path)
            downloaded_videos.append(new_video_path)

