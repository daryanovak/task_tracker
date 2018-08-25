from django import forms
from django.forms import Textarea
from tracker_lib.enums import Status


class TaskForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', widget=Textarea)
    status = forms.ChoiceField(label='Status', choices=[(status.value, status.name) for status in Status])
    tags = forms.CharField(max_length=200, required=False)