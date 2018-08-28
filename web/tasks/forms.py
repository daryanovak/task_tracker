from django import forms
from django.forms import Textarea, SelectDateWidget
from tracker_lib.enums import Status
import datetime


class TaskForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', widget=Textarea)
    start_date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))

    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 10, cur_year + 100)])

    start = forms.DateField(
        widget=SelectDateWidget(
            years=year_range,
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )

    deadline = forms.DateField(
        widget=SelectDateWidget(
            years=year_range,
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )

    status = forms.ChoiceField(label='Status', choices=[(status.value, status.name) for status in Status])
    tags = forms.CharField(max_length=200, required=False)
    parent = forms.CharField(widget=forms.HiddenInput(), required=False)