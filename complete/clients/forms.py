from django import forms

from .models import ClientList

class Clientform(forms.ModelForm):
    class Meta:
        model = ClientList
        fields =[
            'name', 'project_name', 'phno', 'email','team_details',
        ]
