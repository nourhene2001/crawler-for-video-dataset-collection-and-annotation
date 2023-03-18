from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
import os
import signal
import threading
from unittest import signals
from django.shortcuts import render
from scrapy import Spider
from .forms import  QForm
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrape.spiders.youtube import YoutubeSpider
from django.http import HttpResponse, JsonResponse
#fun to run the spider
def run_spider(query):
    process = CrawlerProcess(get_project_settings())
    spider_cls = YoutubeSpider
    process.crawl(spider_cls,query=query)
    process.start()
#the function that takes the query and start the spider
def search(request):
    form=QForm()
    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            p = Process(target=run_spider, args=(query,))
            p.start()
            p.join()
            csv_path = os.path.join(os.getcwd(), '', 'data.csv')
            with open(csv_path,encoding='utf-8') as csv_file:
                response = HttpResponse(csv_file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{query}.csv"'
                return response
        else:
            form = QForm()
    return render(request, 'forms.html', {'form': form})




#function retrieve data 
