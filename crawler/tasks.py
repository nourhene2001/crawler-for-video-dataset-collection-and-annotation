from zipfile import ZipFile
from celery import shared_task
from django.core import serializers

import pytube
import os

@shared_task
def download_videos(instance):
    # Deserialize the instance object
    instance = serializers.deserialize('json', instance, ignorenonexistent=True).next().object
    print('MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')
    videos = instance.videos.all()
    downloaded_videos = []
    for video in videos:
        yt = pytube.YouTube(video.url)
        stream = yt.streams.filter(res=video.resolution, file_extension=video.videoformat).first()
        if stream is not None:
            video_path = stream.download(output_path=instance.folder)
            print(video_path)
            downloaded_videos.append(video_path)
        else:
            stream = yt.streams.filter(res=video.resolution, file_extension="mp4").first()
            video_path = stream.download(output_path=instance.folder)
            print(video_path)
            downloaded_videos.append(video_path)

