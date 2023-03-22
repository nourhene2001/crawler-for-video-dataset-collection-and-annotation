from multiprocessing import Process
import django
import json
django.setup()
import os
from django import apps
from django.shortcuts import render
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrape.spiders.youtube import YoutubeSpider
from .forms import  CheckForm, QForm

from crawler.models import dataModel
#fun to run the spider
def run_spider(query,max_items,duration):
    process = CrawlerProcess(get_project_settings())
    spider_cls = YoutubeSpider
    process.crawl(spider_cls,query=query,max_items=max_items,duration=duration)
    process.start()
#the function that takes the query and start the spider
def search(request):
    form=QForm()
    if request.method == 'POST':
        form = QForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            max_items=form.cleaned_data['max_items']
            duration=form.cleaned_data['duration']
            p = Process(target=run_spider, args=(query,max_items,duration))
            p.start()
            p.join()
            json_path = os.path.join(os.getcwd(), '', 'data.json')
            with open(json_path,encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                title = item['title']
                views = item['views']
                duration = item['duration']
                description = item['description']
                url = item['url']
                new_data = dataModel.objects.create(
                    title=title,
                    views=views,
                    duration=duration,
                    description=description,
                    url=url
                )
                new_data.save()
            form1 = CheckForm() 
            return render(request, 'result.html', {'data': data,'form1': form1})
            """csv_path = os.path.join(os.getcwd(), '', 'data.csv')
            with open(csv_path,encoding='utf-8') as csv_file:
                response = HttpResponse(csv_file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{query}.csv"'
                return response"""
        else:
            form = QForm()
    return render(request, 'forms.html', {'form': form})
