from django.db import models
from accounts.models import *
from django.contrib.auth.models import User
import calendar
from datetime import date

# Create your models here.
class recent_activity(models.Model):

    task_done = models.CharField(max_length = 128)
    dates = models.DateField(blank = True,null = True)
    times = models.TimeField(blank = True,null = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
