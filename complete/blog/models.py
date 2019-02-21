from django.db import models
from django.contrib.auth.models import User
from accounts.models import teamtable

class post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    team_details=models.ForeignKey(teamtable, on_delete=models.CASCADE,default='')

    def __str__(self):
        return str(self.title)

class comment(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE,default='')
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.content)
