from zipfile import ZipFile
from celery import shared_task

import pytube
import os

@shared_task
def download_videos(instance):
    videos = instance.videos.all()
    downloaded_videos = []
    for video in videos:
        yt = pytube.YouTube(video.url)
        stream = yt.streams.filter(res=video.resolution, file_extension=video.videoformat).first()
        if stream is not None:
            video_path = stream.download(output_path=video.folder)
            downloaded_videos.append(video_path)
        else:
            stream = yt.streams.filter(res=video.resolution, file_extension="mp4").first()
            video_path = stream.download(output_path=video.folder)
            downloaded_videos.append(video_path)
    zip_path = os.path.join(video.folder, 'videos.zip')
    with ZipFile(zip_path, 'w') as zip_file:
        for video_path in downloaded_videos:
            video_name = os.path.basename(video_path)
            zip_file.write(video_path, video_name)
