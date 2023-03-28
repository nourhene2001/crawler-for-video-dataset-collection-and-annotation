
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
from .forms import   QForm, dataForm, datasetForm1, datasetForm2
from django.contrib.auth.decorators import login_required
from crawler.models import dataModel, datasetModel
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime
from django.contrib import messages

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
            form2=datasetForm1()
            form3=datasetForm2()
            return render(request, 'result.html', {'data': data,'form1':form1,'form2':form2,'form3':form3})
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
    form1 = datasetForm1()
    form2 = datasetForm2()
    if request.method == 'POST':
        form = dataForm(request.POST)
        selected_elements = request.POST.getlist('selected_elements')
        if form.is_valid():
            videoformat = form.cleaned_data['videoformat']
            resolution = form.cleaned_data['resolution']
            selected_data=dataModel.objects.filter(id__in=selected_elements)
            dataModel.objects.exclude(id__in=selected_elements).delete()
            selected_data.update(videoformat=videoformat, resolution=resolution)
            if 'm1' in request.POST:
                form1 = datasetForm1(request.POST)
                if form1.is_valid() :
                    min_v=form1.cleaned_data.get('min_v')
                    name=form1.cleaned_data.get('form1_name')
                    if selected_data.count() > int(min_v):
                        new_obj = datasetModel.objects.create(
                            name=name,
                            creation_date=datetime.now(),
                            num_video=selected_data.count() ,
                            min_v=min_v
                        )
                        new_obj.save()
                        for i in selected_elements:
                            new_obj.videos.add(i)
                        for data in selected_data:
                            data.datasets.add(new_obj)
                        return redirect('check')
                    else:
                            #alert the user
                        messages.error(request, 'Error message.')
                        return redirect('check')
            elif 'm2' in request.POST:
                form2 = datasetForm2(request.POST)
                if form2.is_valid():
                    name=form2.cleaned_data.get('form2_name')
                    print(name)
                    model=datasetModel.objects.get(name=name)
                    model.num_video += selected_data.count()
                    model.save()
                    for data in selected_data:
                        data.datasets.add(model)
                    for data in model.videos.all():
                        data.videos.add(selected_data)
                    return redirect('check')
             
    else:
        data = dataModel.objects.all()
    return render(request, 'result.html')
#for form of datasets:

#register view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
#login view
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
#logout view
def logout(request):
    auth_logout(request)
    return redirect('search')

                

