from django import forms
from .models import post, comment

class postform(forms.ModelForm):

    class Meta:
        model=post
        fields=('title', 'content',)

class commentform(forms.ModelForm):

    class Meta:
        model=comment
        fields=('content',)
