
from multiprocessing import Process
import django
import json

from django.http import HttpResponse, JsonResponse
from httplib2 import Authentication
django.setup()
import os
from django import apps
from django.shortcuts import redirect, render
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrape.spiders.youtube import YoutubeSpider
from .forms import   QForm, dataForm, datasetForm1, datasetForm2, datasetForm3
from django.contrib.auth.decorators import login_required
from crawler.models import  dataModel, datasetModel, video_dataset
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

#fun to run the spider
def run_spider(query,max_items,duration):
    process = CrawlerProcess(get_project_settings())
    spider_cls = YoutubeSpider
    process.crawl(spider_cls,query=query,max_items=max_items,duration=duration)
    process.start()
@login_required
@csrf_exempt
def update_dataset(request):
    print('§§§§§§§§§§§§§§§§§§§§s')
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        data = json.loads(request.body)
        data_id = data.get('data_id')
        field_name = data.get('field_name')
        field_value = data.get('field_value')
        print(field_value)
        dataset = datasetModel.objects.get(id=data_id)
        setattr(dataset, field_name, field_value)
        dataset.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
@login_required
def display_dataset(request):
    data=datasetModel.objects.all()
    print(data)
    return render(request, 'update_dataset.html', {'data': data})
#main page
@login_required
def main(request):
    return render(request,'main.html')
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
            c=0
             # get the time when the form was submitted
            for item in data:
                new_data = dataModel.objects.create(
                    
                    title=item['title'],
                    views=item['views'],
                    duration=item['duration'],
                    description=item['description'],
                    url=item['url']
                )
                c=c+1
                new_data.save()
    

            form1=dataForm()
            
            form3=datasetForm3()
            return render(request, 'result.html', {'data': dataModel.objects.all().order_by('-id')[:c],'form1':form1,'form3':form3})
            """csv_path = os.path.join(os.getcwd(), '', 'data.csv')
            with open(csv_path,encoding='utf-8') as csv_file:
                response = HttpResponse(csv_file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{query}.csv"'
                return response"""
        else:
            form = QForm()
    return render(request, 'forms.html', {'form': form})
#create the dataset
@login_required
def create_d(request):
    form_create=datasetForm1()
    if request.method == 'POST':
        form_create=datasetForm1(request.POST)
        if form_create.is_valid():
            name=form_create.cleaned_data['form1_name']
            min_v=form_create.cleaned_data['min_v']
            max_v=form_create.cleaned_data['max_v']
            description=form_create.cleaned_data['description']
            new_obj = datasetModel.objects.create(
                            name=name,
                            creation_date=datetime.now(),
                            min_v=min_v,
                            max_v=max_v,
                            description=description
                        )
            new_obj.save()
    return render(request, 'new_dataset.html',{'form_create': form_create})
#choose the dataset to update
"""@login_required
def update_d(request):
    form3=datasetForm3()
    if request.method == 'POST':
        form3 = datasetForm3(request.POST)
        if form3.is_valid():
            name=form3.cleaned_data['form3_name']
            return redirect('update', name=name)
    return render(request,'update_dataset.html', {'form3': form3})
#update the dataset
@login_required
def update(request,name):
    i = datasetModel.objects.get(name=name)
    id=i.id
    instance=datasetModel.objects.get(id=id)
    form2 = datasetForm2(instance=instance)
    if request.method == 'POST':
        print('§§§§§§§§§§§§§§§§§§§§§§§§§§§§')
        form2 = datasetForm2(request.POST, instance=instance)
        if form2.is_valid():
            name=form2.cleaned_data['form2_name']
            min_v=form2.cleaned_data['min_v']
            max_v=form2.cleaned_data['max_v']
            description=form2.cleaned_data['description']
            instance.update(name=name,min_v=min_v,max_v=max_v,description=description)
            instance.save()
    return render(request,'update_dataset.html', {'form2': form2})"""
#after result page choose
@login_required
def choice_d(request):
    form = dataForm()
    form2=datasetForm3
    if request.method=='POST':
        form2=datasetForm3(request.POST)
        selected_elements = request.POST.getlist('selected_elements')
        if form.is_valid() and form2.is_valid:
            videoformat = form.cleaned_data['videoformat']
            resolution = form.cleaned_data['resolution']
            selected_data=dataModel.objects.filter(id__in=selected_elements)
            print(selected_data)
            selected_data.update(videoformat=videoformat, resolution=resolution)
            if form2.is_valid():
                name=form2.cleaned_data.get('form3_name')
                model=datasetModel.objects.get(name=name)
                model.num_video += selected_data.count()
                model.save()
                for v in selected_data:
                    v_d = video_dataset.objects.create(dataset=model, videos=v)
                v_d.save()
                return render(request, 'main.html')
    return render(request,'result.html')
"""@login_required
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
            print(selected_data)
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
                        for v in selected_data:
                            v_d = video_dataset.objects.create(dataset=new_obj, videos=v)
                        v_d.save()
                        return render(request, 'new_dataset.html')
                    else:
                            #alert the user
                        messages.error(request, 'Error message.')
                        return redirect('check')
            elif 'm2' in request.POST:
                form2 = datasetForm2(request.POST)
                if form2.is_valid():
                    name=form2.cleaned_data.get('form2_name')
                    model=datasetModel.objects.get(name=name)
                    model.num_video += selected_data.count()
                    

                    model.save()
                    for v in selected_data:
                            v_d = video_dataset.objects.create(dataset=model, videos=v)
                    v_d.save()
                    return render(request, 'update_dataset.html')
             
    else:
        data = dataModel.objects.all()
    return render(request, 'result.html')"""
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
    return redirect('welcome')
def welcome(request):
    return render(request,'welcome.html')
@login_required
def delete(request):
    if request.method=='post':
        d_id = request.POST.get('id')
        print('!!!!!!!!!!')
        print(d_id)
        dataset = datasetModel.objects.get(id=d_id)
        dataset.delete()
        data = datasetModel.objects.all()
        return render(request,'update_dataset.html',{'data': data})

    else:
       data=datasetModel.objects.all()
       return render(request, 'update_dataset.html', {'data': data}) 
                

