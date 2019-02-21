from django.db import models
from django.contrib.auth.models import User
from accounts.models import teamtable

# Create your models here.
class check_date(models.Model):
    date = models.DateField()
    work_title = models.CharField(max_length=34)
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE)


class check_date1(models.Model):
    date = models.DateField()
    work_title = models.CharField(max_length=34)
    team_details=models.ForeignKey(teamtable,default='',on_delete=models.CASCADE)

