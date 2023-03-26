from django import forms
from crawler.models import dataModel, datasetModel
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
   #new dataset
class datasetForm1(forms.ModelForm):
    class Meta:
        model=datasetModel
        fields={"name"}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dataset name'}),
        }
        #when he wants to store in an existing dataset
class datasetForm2(forms.ModelForm):
    name = forms.ChoiceField(choices=[])
    class Meta :
        model = datasetModel
        fields={"name"}
    def __init__(self):
        super().__init__()
        name =datasetModel.objects.values_list('name', flat=True)
        choices = [(m, m) for m in name]
        self.fields['name'].choices = choices


