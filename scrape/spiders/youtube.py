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
    def __init__(self, query, max_items,duration):
        super().__init__(query)
        self.query=query
        self.max_items=max_items
        self.duration=duration
    
         
    #start_url should be result of that query
    def start_requests(self):
        youtube=build('youtube', 'v3', developerKey=os.environ.get('AIzaSyAcqH635cbFPKvQX_66XaMtGxENrGKggeo'))
        
        search_response = youtube.search().list(
        q=self.query,
        type='video',
        #the parts of the resource to be returned in the API response
        part='id,snippet',
        videoDuration=self.duration,
        #to be changed later !!!!!!!!!!!!!!!!!
        maxResults=min(self.max_items, 50),
        ).execute()
        self.next_page_token = search_response.get('nextPageToken')
        video_ids = []
        for search_result in search_response.get('items', []):
                video_ids.append(search_result['id']['videoId'])

        for video_id in video_ids:
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            yield scrapy.Request(video_url, callback=self.parse_video)
        # Make additional requests if there are more results
        while self.next_page_token and len(video_ids) < self.max_items:
            search_request = youtube.search().list(
                q=self.query,
                type='video',
                part='id,snippet',
                videoDuration=self.duration,
                maxResults=min(self.max_items - len(video_ids), 50),
                pageToken=self.next_page_token,
            )
            search_response = search_request.execute()
            self.next_page_token = search_response.get('nextPageToken')
            video_ids.extend([search_result['id']['videoId'] for search_result in search_response.get('items', [])])

            for video_id in video_ids:
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                yield scrapy.Request(video_url, callback=self.parse_video)
        
    #scrape additional info with pytube and download the video
    def parse_video(self, response):
        items=ScrapeItem()
        #url response from parse method
        try:
            video_url = response.url
                #youtube obj with the video url provided
            yt = YouTube(video_url)
                #we extract the needed infos
            id_vid=yt.video_id
            title=yt.title
            views = yt.views
            duration = yt.length
            description = yt.description
            items['id_vid']=id_vid
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
        

