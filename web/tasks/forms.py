import datetime

from django import forms
from django.forms import Textarea, DateTimeInput
from tracker_lib.enums import Status


class TaskForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(label='Text', widget=Textarea)

    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year - 10, cur_year + 100)])

    date = forms.DateTimeField(
        label='Deadline',
        help_text='Use "d/M/Y H:M" format, for example "22/12/2011 12:42"',
        input_formats=('%d/%m/%y %H:%M',),
        required=False
    )

    status = forms.ChoiceField(label='Status', choices=[(status.value, status.name) for status in Status])
    tags = forms.CharField(max_length=200, required=False)
    is_periodic = forms.BooleanField(
        label='Is Periodic',
        widget=forms.CheckboxInput(),
        required=False
    )

    period = forms.CharField(
        label='Period',
        required=False,
    )

    start_date = forms.DateTimeField(
        label='Start Date',
        input_formats=('%d/%m/%y %H:%M',),
        required=False,
    )
