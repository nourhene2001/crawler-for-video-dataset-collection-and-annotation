from django import forms

class QForm(forms.Form):
    query = forms.CharField(max_length=50)
    #content_type = forms.BooleanField(label='content type', required=False)
    #Media_size= forms.BooleanField(label='Media size', required=False)
    #still in progess
    OPTIONS = [('1', 'MP4'), ('2', 'AVI'), ('3', 'WebM'),('3', '3GP'),('3', 'FLV'),('3', 'MKV')]
    video_format = forms.ChoiceField(choices=OPTIONS)
    max_result = forms.IntegerField()

    

    
