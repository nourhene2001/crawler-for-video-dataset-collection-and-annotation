from django import forms

class QForm(forms.Form):
    query = forms.CharField(max_length=50)
    content_type = forms.BooleanField(label='content type', required=False)
    Media_size= forms.BooleanField(label='Media size', required=False)
    video_format = forms.BooleanField(label='video format', required=False)
    max_result = forms.BooleanField(label='maximum number of result', required=False)

    
