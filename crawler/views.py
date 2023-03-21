from concurrent.futures import ThreadPoolExecutor
import json
from multiprocessing import Process, Manager
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
def run_spider(query,max_result,duration):
    process = CrawlerProcess(get_project_settings())
    spider_cls = YoutubeSpider
    process.crawl(spider_cls,query=query,max_result=max_result,duration=duration)
    process.start()
    """json_path = os.path.join(os.getcwd(), '', 'data.json')
    with open(json_path, 'r') as f:
        result_data = f.read()
    return result_data"""

#the function that takes the query and start the spider
def search(request):
    form=QForm()
    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            max_result=form.cleaned_data['max_result']
            duration=form.cleaned_data['duration']
            p = Process(target=run_spider, args=(query,max_result,duration))
            p.start()
            p.join()
            json_path = os.path.join(os.getcwd(), '', 'data.json')
            with open('data.json', 'r') as f:
                data = json.load(f)
            return render(request, 'result.html', {'data': data})
            """csv_path = os.path.join(os.getcwd(), '', 'data.csv')
            with open(csv_path,encoding='utf-8') as csv_file:
                response = HttpResponse(csv_file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{query}.csv"'
                return response"""
        else:
            form = QForm()
    return render(request, 'forms.html', {'form': form})
#function retrieve data 