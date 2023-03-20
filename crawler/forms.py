from django import forms

class QForm(forms.Form):
    query = forms.CharField(max_length=50)
    #content_type = forms.BooleanField(label='content type', required=False)
    #Media_size= forms.BooleanField(label='Media size', required=False)
    #still in progess
    OPTIONS = ['any','short','medium','long']
    duration = forms.ChoiceField(choices=[(choice, choice) for choice in OPTIONS])
    max_result = forms.IntegerField()
    #min_duration=forms.CharField()
    #max_duration=forms.CharField()

    

    
