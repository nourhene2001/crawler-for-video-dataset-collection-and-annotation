import os
import scrapy
import pytube
from pytube import YouTube
from googleapiclient.discovery import build

from scrape.items import ScrapeItem
class YoutubeSpider(scrapy.Spider):
    name = "youtube"
    allowed_domains = ["youtube.com"]
    

    #set up the initial state of the spider , take the query as argument
     #query from the django app
    def __init__(self, query, max_result,duration):
        super().__init__(query)
        self.query=query
        self.max_result=max_result
        self.duration=duration
    
         
    #start_url should be result of that query
    def start_requests(self):
        youtube=build('youtube', 'v3', developerKey=os.environ.get('AIzaSyCt4dh_uoZ7rncyiftsOl4rmhksZ4w8eJ4'))
        
        search_response = youtube.search().list(
        q=self.query,
        type='video',
        #the parts of the resource to be returned in the API response
        part='id,snippet',
        videoDuration=self.duration,
        #to be changed later !!!!!!!!!!!!!!!!!
        maxResults=self.max_result
        ).execute()
        video_ids = []
        for search_result in search_response.get('items', []):
                video_ids.append(search_result['id']['videoId'])

        for video_id in video_ids:
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            yield scrapy.Request(video_url, callback=self.parse_video)
        # Make a request to a URL and execute the parse method when the response is received
        #specify the URL to request, the callback function to be executed when the response is received
        
    #scrape additional info with pytube and download the video
    def parse_video(self, response):
        items=ScrapeItem()
        #url response from parse method
        try:
            video_url = response.url
                #youtube obj with the video url provided
            yt = YouTube(video_url)
                #we extract the needed infos
            title=yt.title
            views = yt.views
            duration = yt.length
            description = yt.description
            items['title']=title
            items['views']=views
            items['duration']=duration
            items['description']=description
            items['url']=video_url
                #stream = yt.streams.get_highest_resolution()
                #stream=yt.streams.filter(file_extension='self.video_format')
            # Download the video
                #stream.download()
        except pytube.exceptions.VideoUnavailable:
        # Handle the exception - skip this video
            print(f"Video at URL  is unavailable. Skipping...")
        #stream = yt.streams.get_highest_resolution()
        #stream=yt.streams.filter(file_extension='self.video_format')
        # Download the video
        #stream.download()
        yield items
        


