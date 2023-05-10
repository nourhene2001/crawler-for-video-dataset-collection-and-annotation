import json
from zipfile import ZipFile
from celery import shared_task
from django import apps
from django.core import serializers

import pytube
import os
from crawler.annotate_try2 import annotate_vid

from crawler.models import datasetModel

@shared_task
def download_videos(pk):
    print('MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMk')
    instance=datasetModel.objects.get(pk=pk)
    print('MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')
    videos = instance.videos.all()
    fi=instance.folder+"\\"+instance.name
    print("hhhhhhhhhhhhhhhhhhhhhhhhhh")
    print(fi)
    f=instance.folder+"\\"+instance.name+"\\videos"
    downloaded_videos = []
    
    for video in videos:
        i=0
        yt = pytube.YouTube(video.url)
        stream = yt.streams.filter(res=instance.resolution, file_extension=instance.videoformat).first()
        if stream is not None:
                            try:
                                video_path = stream.download(output_path=f)
                                
                            except Exception:
                                # Get the list of all files in the folder and sort them by creation time
                                all_files = os.listdir(f)
                                all_files.sort(key=lambda x: os.path.getctime(os.path.join(f, x)))

                                # Get the latest added file and delete it
                                latest_file = os.path.join(f, all_files[-1])
                                os.remove(latest_file)
                                
                                continue
                                # Rename the downloaded video file to i+1
                            i=i+1
                            new_video_path = os.path.join(f, f"{i}.{instance.videoformat}")
                            
                            os.rename(video_path, new_video_path)

                            downloaded_videos.append(new_video_path)
                            
                            instance.save()
                            annotate_vid(fi,instance.author,video.duration,instance.creation_date,instance.resolution,instance.videoformat,video.views,instance.name,video.description,instance.description)
        else:
            stream = yt.streams.filter(res=instance.resolution, file_extension="mp4").first()
            video_path = stream.download(output_path=f)
            print(video_path)
            i=0
                            # Rename the downloaded video file to i+1
            new_video_path = os.path.join(f, f"{i}.mp4")
            os.rename(video_path, new_video_path)
            downloaded_videos.append(new_video_path)
            instance.save()
            annotate_vid(fi,instance.author,video.duration,instance.creation_date,instance.resolution,instance.videoformat,video.views,instance.name,video.description,instance.description)

