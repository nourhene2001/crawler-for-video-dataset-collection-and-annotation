from multiprocessing import Process
import django
import json

from django.http import HttpResponse
from httplib2 import Authentication
django.setup()
import os
from django import apps
from django.shortcuts import redirect, render
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrape.spiders.youtube import YoutubeSpider
from .forms import   QForm, dataForm
from django.contrib.auth.decorators import login_required
from crawler.models import dataModel
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


#fun to run the spider
def run_spider(query,max_items,duration):
    process = CrawlerProcess(get_project_settings())
    spider_cls = YoutubeSpider
    process.crawl(spider_cls,query=query,max_items=max_items,duration=duration)
    process.start()
#the function that takes the query and start the spider
@login_required
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
            dataModel.objects.all().delete()
            for item in data:
                new_data = dataModel.objects.create(
                    
                    title=item['title'],
                    views=item['views'],
                    duration=item['duration'],
                    description=item['description'],
                    url=item['url']
                )
                new_data.save()
               
                data=dataModel.objects.all()
            form1=dataForm()
            return render(request, 'result.html', {'data': data,'form1':form1})
            """csv_path = os.path.join(os.getcwd(), '', 'data.csv')
            with open(csv_path,encoding='utf-8') as csv_file:
                response = HttpResponse(csv_file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{query}.csv"'
                return response"""
        else:
            form = QForm()
    return render(request, 'forms.html', {'form': form})
@login_required
def check(request):
    form = dataForm()
    if request.method == 'POST':
        form = dataForm(request.POST)
        if form.errors:
            print(form.errors)
        selected_elements = request.POST.getlist('selected_elements')
        print(selected_elements)
        if form.is_valid():
            videoformat = form.cleaned_data['videoformat']
            resolution = form.cleaned_data['resolution']
            print(videoformat)
            dataModel.objects.exclude(id__in=selected_elements).delete()
            dataModel.objects.filter(id__in=selected_elements).update(videoformat=videoformat, resolution=resolution)
            data = dataModel.objects.all()
            return render(request, 'result.html', {'data': data,'form1':form})
    else:
        data = dataModel.objects.all()
        
    return render(request, 'result.html')
    

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('search')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('search')

                

