from django import forms

from .models import MyTodoList

class MyTodoform(forms.ModelForm):
    class Meta:
        model = MyTodoList
        fields =[
            'title', 'due_date'
        ]