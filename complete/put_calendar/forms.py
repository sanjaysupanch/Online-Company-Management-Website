from django import forms

from .models import *

class EventForm(forms.ModelForm):
    class Meta:
        model = check_date
        fields =[
            'date', 'work_title',
        ]

class GroupForm(forms.ModelForm):
    class Meta:
        model = check_date1
        fields =[
            'date','work_title','team_details',
        ]

