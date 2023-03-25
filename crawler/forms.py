from django import forms
from crawler.models import dataModel
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.forms import AuthenticationForm
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

    



