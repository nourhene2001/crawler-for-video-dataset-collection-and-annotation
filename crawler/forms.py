from django import forms
from crawler.models import dataModel, datasetModel
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import FileExtensionValidator
from tkinter import Tk, filedialog
class QForm(forms.Form):
    query = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'what are you looking for ?'}))
    #content_type = forms.BooleanField(label='content type', required=False)
    #Media_size= forms.BooleanField(label='Media size', required=False)
    #still in progess
    max_items = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'MAX ITEMS'}))
    OPTIONS = ['any','short','medium','long']
    duration = forms.ChoiceField(choices=[(choice, choice) for choice in OPTIONS])
   
    #min_duration=forms.CharField()
    #max_duration=forms.CharField()

class dataForm(forms.ModelForm):
    class Meta:
        model= dataModel
        fields={"videoformat","resolution"} 
        widgets = {
            'videoformat': forms.Select(choices=dataModel.OPTIONS1,attrs={'required': True}),
            'resolution': forms.Select(choices=dataModel.OPTIONS2,attrs={'required': True}),
            
        }



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

#create

class datasetForm1(forms.ModelForm):
    
    class Meta:
        model = datasetModel
        fields = ("name", "min_v","max_v","description","folder","author","desired_num")
        labels = {
            
            'min_v': 'minimum number of videos',
            'max_v': 'maximum number of videos',
            'desired_num': 'desired number of videos',
            'folder':'folder path',

        }
        widgets = {
            
            'min_v': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'minimum number of videos', 'required': False}),
            'max_v': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'maximum number of videos', 'required': False}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description..', 'required': True}),
            'folder':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'where your videos will be stored.. ', 'required': True}),
        }


    """def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['form1_name']
        
    
        if commit:
            instance.save()
        return instance"""
#update
class datasetForm2(forms.ModelForm):
    OPTIONS = [('in progress',"in progress"),('completed',"completed")]
    status = forms.ChoiceField(label='status', choices=OPTIONS, required=True, widget=forms.Select(attrs={'required': False}))
    
    class Meta:
        model = datasetModel
        fields = ("name","description","id", "min_v","max_v","description","desired_num","status","author","folder")
        labels = {
            'min_v': 'minimum number of videos',
            'max_v': 'maximum number of videos',
            'desired_num': 'desired number of videos',
            'folder':'folder path',

            

        }
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'hidden': True}),
            'min_v': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'min vid', 'required': False}),
            'max_v': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'max vid', 'required': False}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description', 'required': False}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'author', 'required': False}),

        }



    def save(self, commit=True):
        instance = super().save(commit=False)
        
        instance.status = self.cleaned_data['status']
        if commit:
            instance.save()
        return instance
#choose the one to update
class datasetForm3(forms.ModelForm):
    form3_name = forms.ChoiceField(label='form3_name', choices=[], required=True, widget=forms.Select(attrs={'required': True}))
    
    class Meta:
        model = datasetModel
        fields = ["form3_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        name_choices = datasetModel.objects.values_list('name', flat=True)
        choices = [('', '---')] +[(m, m) for m in name_choices]
        self.fields['form3_name'].choices = choices

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['form3_name']
        if commit:
            instance.save()
        return instance
    
