from django import forms
from crawler.models import dataModel, datasetModel
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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
    form1_name = forms.CharField(label='form1_name', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dataset name','required': False}))

    class Meta:
        model = datasetModel
        fields = ("form1_name", "min_v","max_v","description")
        widgets = {
            'min_v': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'min vid', 'required': False}),
            'max_v': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'max vid', 'required': False}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description', 'required': False})
        }


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['form1_name']
        if commit:
            instance.save()
        return instance
#update
class datasetForm2(forms.ModelForm):
    form2_name = forms.ChoiceField(label='form2_name', choices=[], required=False, widget=forms.Select(attrs={'required': False}))
    widgets = {
            'min_v': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'min vid', 'required': False}),
            'max_v': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'max vid', 'required': False}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description', 'required': False})
        }
    class Meta:
        model = datasetModel
        fields = ("form2_name", "min_v","max_v","description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        name_choices = datasetModel.objects.values_list('name', flat=True)
        choices = [('', '---')] +[(m, m) for m in name_choices]
        self.fields['form2_name'].choices = choices

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['form2_name']
        if commit:
            instance.save()
        return instance
#choose the one to update
class datasetForm3(forms.ModelForm):
    form3_name = forms.ChoiceField(label='form3_name', choices=[], required=True, widget=forms.Select(attrs={'required': False}))
    widgets = {
            
        }
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